import secrets
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from httpx2 import AsyncClient
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend_app.core.authenticate import Authenticate
from backend_app.core.jwt import Token
from backend_app.core.security import Password
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep, db

router = APIRouter()

AUTHORIZE_URL = "https://api.intra.42.fr/oauth/authorize"
TOKEN_URL = "https://api.intra.42.fr/oauth/token"
ME_URL = "https://api.intra.42.fr/v2/me"
USERNAME_MAX = 32


async def unique_username(base: str, session) -> str:
    base = base[: USERNAME_MAX - 5]
    candidate = base
    while await session.scalar(
        select(UserModel.id).where(UserModel.username == candidate)
    ):
        candidate = f"{base}_{secrets.token_hex(2)}"
    return candidate


@router.get("/login_with_42")
async def login_with_42():
    state = secrets.token_urlsafe(32)

    params = {
        "client_id": db.settings.FORTYTWO_CLIENT_ID,
        "redirect_uri": db.settings.FORTYTWO_REDIRECT_URI,
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

    if not state or not saved_state or not secrets.compare_digest(state, saved_state):
        raise HTTPException(status_code=400, detail="Invalid OAuth State")

    async with AsyncClient() as client:
        token_response = await client.post(
            TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": db.settings.FORTYTWO_CLIENT_ID,
                "client_secret": db.settings.FORTYTWO_CLIENT_SECRET,
                "code": code,
                "redirect_uri": db.settings.FORTYTWO_REDIRECT_URI,
            },
        )
        if token_response.status_code != 200:
            print(f"[callback] token error: {token_response.text}")
            raise HTTPException(status_code=502, detail="Token Error")

        access_token = token_response.json().get("access_token")
        if not access_token:
            raise HTTPException(status_code=502, detail="Token Error")

        me_response = await client.get(
            ME_URL, headers={"Authorization": f"Bearer {access_token}"}
        )

    if me_response.status_code != 200:
        print(f"[callback] me error: {me_response.text}")
        raise HTTPException(status_code=502, detail="Response Error")

    user_data = me_response.json()
    email = (user_data.get("email") or "").strip().lower()
    if not email or email.count("@") != 1:
        raise HTTPException(status_code=400, detail="No email provided by 42 API")

    login = user_data.get("login") or email.split("@")[0]
    medium_img = ((user_data.get("image") or {}).get("versions") or {}).get("medium")

    user = await Authenticate.get_user(email, session)

    if user is None:
        new_user = UserModel(
            email=email,
            hashed_password=Password.hash_password(secrets.token_urlsafe(32)),
            username=await unique_username(login, session),
            picture=medium_img,
            email_verified=True,
        )
        session.add(new_user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Could not create account, please retry",
            )
    elif not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="An account with this email already exists. Log in with your password.",
        )

    redirect = RedirectResponse(url=f"{db.settings.FRONTEND_URL.rstrip('/')}/profile")
    redirect.delete_cookie("oauth_state", path="/")
    Token.generate_token(email, redirect)
    return redirect