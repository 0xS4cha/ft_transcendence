import logging
import re
import secrets
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from httpx2 import AsyncClient, HTTPError
from sqlalchemy.exc import IntegrityError

from backend_app.core.authenticate import Authenticate
from backend_app.core.jwt import Token
from backend_app.core.security import Password
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep, db

logger = logging.getLogger(__name__)

router = APIRouter()

AUTHORIZE_URL = "https://api.intra.42.fr/oauth/authorize"
TOKEN_URL = "https://api.intra.42.fr/oauth/token"
ME_URL = "https://api.intra.42.fr/v2/me"
USERNAME_MAX = 32
UPSTREAM_TIMEOUT_SECONDS = 10


async def unique_username(base: str, session) -> str:
    base = re.sub(r"[^A-Za-z0-9_-]", "", base)[: USERNAME_MAX - 5]
    if len(base) < 3:
        base = f"user{base}"
    candidate = base
    while await Authenticate.username_taken(candidate, session):
        candidate = f"{base}_{secrets.token_hex(2)}"
    return candidate


def upstream_error(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)


@router.get("/login_with_42")
async def login_with_42():
    state = secrets.token_urlsafe(32)

    params = {
        "client_id": db.settings.FORTYTWO_CLIENT_ID,
        "redirect_uri": str(db.settings.FORTYTWO_REDIRECT_URI),
        "response_type": "code",
        "state": state,
    }

    response = RedirectResponse(url=f"{AUTHORIZE_URL}?{urlencode(params)}")
    response.set_cookie(
        key="oauth_state",
        value=state,
        max_age=600,
        path="/",
        secure=db.settings.FORTYTWO_REDIRECT_URI.scheme == "https",
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/login_with_42/callback")
async def callback(
    request: Request,
    session: AsyncSessionDep,
    code: str | None = None,
    state: str | None = None,
) -> Response:
    saved_state = request.cookies.get("oauth_state")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    if not state or not saved_state or not secrets.compare_digest(
        state.encode(), saved_state.encode()
    ):
        raise HTTPException(status_code=400, detail="Invalid OAuth State")

    try:
        async with AsyncClient(timeout=UPSTREAM_TIMEOUT_SECONDS) as client:
            token_response = await client.post(
                TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "client_id": db.settings.FORTYTWO_CLIENT_ID,
                    "client_secret": db.settings.FORTYTWO_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": str(db.settings.FORTYTWO_REDIRECT_URI),
                },
            )
            if token_response.status_code != 200:
                logger.warning(f"[callback] token error: {token_response.status_code}")
                raise upstream_error("Token Error")

            access_token = token_response.json().get("access_token")
            if not access_token:
                raise upstream_error("Token Error")

            me_response = await client.get(
                ME_URL, headers={"Authorization": f"Bearer {access_token}"}
            )
            if me_response.status_code != 200:
                logger.warning(f"[callback] me error: {me_response.status_code}")
                raise upstream_error("Response Error")

            user_data = me_response.json()
    except (HTTPError, ValueError, AttributeError) as e:
        logger.warning(f"[callback] 42 API unavailable: {e!r}")
        raise upstream_error("42 API unavailable") from e

    if not isinstance(user_data, dict):
        raise upstream_error("Response Error")

    email = (user_data.get("email") or "").strip().lower()
    if not email or email.count("@") != 1:
        raise HTTPException(status_code=400, detail="No email provided by 42 API")

    login = user_data.get("login") or email.split("@")[0]
    image = user_data.get("image")
    versions = image.get("versions") if isinstance(image, dict) else None
    medium_img = versions.get("medium") if isinstance(versions, dict) else None

    user = await Authenticate.get_user(email, session)

    if user is None:
        user = UserModel(
            email=email,
            hashed_password=Password.hash_password(secrets.token_urlsafe(32)),
            username=await unique_username(str(login), session),
            picture=medium_img,
            email_verified=True,
        )
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Could not create account, please retry",
            ) from None
        await session.refresh(user)
    elif user.email_verified is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="An account with this email already exists. Log in with your password.",
        )

    redirect = RedirectResponse(url=f"{db.settings.FRONTEND_URL.rstrip('/')}/profile")
    redirect.delete_cookie("oauth_state", path="/")
    Token.generate_token(user, redirect)
    return redirect
