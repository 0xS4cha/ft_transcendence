from fastapi import APIRouter, Response

router = APIRouter()

@router.post("/logout")
async def logout(
    response: Response
) -> None:
    response.delete_cookie(
        key="access_token",
        path="/"
    )
