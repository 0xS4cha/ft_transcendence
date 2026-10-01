from fastapi import APIRouter, HTTPException, status

from backend_app.core.dependencies import RedisDep
from backend_app.schemas.augment import Augment
from backend_app.services.fetch_game_data import get_or_fetch
from backend_app.services.get_augments import (
    AugmentsUnavailableError,
    augments_adapter,
    get_augments,
)

router = APIRouter()

@router.get(
        "/augments_data",
        response_model=list[Augment])
async def get_augments_data(
    r: RedisDep
) -> list[Augment]:
    key = "metatft:augments"

    try:
        augments = await get_or_fetch(r, key, augments_adapter, lambda: get_augments(r))
    except AugmentsUnavailableError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e)
        ) from e

    return augments