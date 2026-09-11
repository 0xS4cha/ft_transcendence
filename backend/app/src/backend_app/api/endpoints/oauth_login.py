import secrets

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from httpx2 import AsyncClient

from backend_app.core.jwt import Token
from shared.database import db

router = APIRouter()

AUTHORIZE_URL = "https://api.intra.42.fr/oauth/authorize"
TOKEN_URL = "https://api.intra.42.fr/oauth/token"
ME_URL = "https://api.intra.42.fr/v2/me"

@router.post("/")
async def login_with_42(
):
    state = secrets.token_urlsafe(32)

    url = (f"{AUTHORIZE_URL}"
           f"?client_id={db.settings.FORTYTWO_CLIENT_ID}"
           f"&redirect_uri={db.settings.FORTYTWO_REDIRECT_URI}"
           f"&response_type=code&state={state}"
    )

    response = RedirectResponse(url=url)

    response.set_cookie(
        key="oauth_state",
        value=state,
        max_age=Token.access_token_expire_minutes*60,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax"
    )

    return response

@router.post("/callback")
async def callback(
    request: Request,
    code: str | None = None,
    state: str | None = None 
) -> JSONResponse:
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

    user = me_response.json()

    return JSONResponse({
        "message": "Successfully logged in with 42",
        "user": user
    })