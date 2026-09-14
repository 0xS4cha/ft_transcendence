import secrets
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from httpx2 import AsyncClient

from backend_app.core.authenticate import Authenticate
from backend_app.core.jwt import Token
from backend_app.core.security import Password
from backend_app.models.user import UserModel
from shared.database import AsyncSessionDep, db

router = APIRouter()

AUTHORIZE_URL = "https://api.intra.42.fr/oauth/authorize"
TOKEN_URL = "https://api.intra.42.fr/oauth/token"
ME_URL = "https://api.intra.42.fr/v2/me"

@router.get("/")
async def login_with_42(
):
    state = secrets.token_urlsafe(32)

    params = {
           "client_id": db.settings.FORTYTWO_CLIENT_ID,
           "redirect_uri": db.settings.FORTYTWO_REDIRECT_URI,
           "response_type": "code",
           "state": state
    }

    url = f"{AUTHORIZE_URL}?{urlencode(params)}"

    response = RedirectResponse(url=url)

    response.set_cookie(
        key="oauth_state",
        value=state,
        max_age=Token.access_token_expire_minutes*60,
        path="/",
        secure=db.settings.FORTYTWO_REDIRECT_URI.scheme == "https",
        httponly=True,
        samesite="lax"
    )

    return response

@router.get("/callback")
async def callback(
    request: Request,
    session: AsyncSessionDep,
    code: str | None = None,
    state: str | None = None 
) -> Response:
    saved_state = request.cookies.get("oauth_state")

    if not code:
        raise HTTPException(
            status_code=400,
            detail="42 did not send an authorization code"
        )

    if not state or state != saved_state:
        raise HTTPException(
            status_code=400,
            detail="Invalid OAuth State"
        )

    async with AsyncClient() as client:
        token_response = await client.post(
            TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": db.settings.FORTYTWO_CLIENT_ID,
                "client_secret": db.settings.FORTYTWO_CLIENT_SECRET,
                "code": code,
                "redirect_uri": db.settings.FORTYTWO_REDIRECT_URI,
            }
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=token_response.status_code,
                detail=token_response.text
            )

        token_data = token_response.json()
        access_token = token_data["access_token"]

        me_response = await client.get(
            ME_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

    if me_response.status_code != 200:
        raise HTTPException(
            status_code=me_response.status_code,
            detail=me_response.text
        )

    user_data = me_response.json()
    email = user_data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="No email provided by 42 API")

    user = await Authenticate.get_user(email, session)
    if not user:
        random_password = secrets.token_urlsafe(32)
        new_user = UserModel(
            email=email,
            hashed_password=Password.hash_password(random_password)
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

    redirect_url = f"{db.settings.FRONTEND_URL.rstrip('/')}/profile"
    redirect = RedirectResponse(url=redirect_url)
    Token.generate_token(email, redirect)

    return redirect