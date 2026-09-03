from fastapi import APIRouter
from ... import database, shared
from sqlalchemy import MetaData, Table, select, inspect

router = APIRouter(
    prefix="/game_data/champions",
    tags=["champions"],
)


@router.get("/{champion_id}")
async def get_champion(champion_id: int):    
    async with database.Session() as session:
        async with session.begin():
            champion = await session.get(shared.models.Champion, champion_id)

            print("champion:", champion)
            print("type:", type(champion))
            print("dict:", vars(champion) if champion else None)
            
            if champion:
                return {
                    column.key: getattr(champion, column.key)
                    for column in inspect(champion).mapper.column_attrs
                }
            return {'status': 'not found'}
