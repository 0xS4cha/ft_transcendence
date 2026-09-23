import asyncio
import sys

import aiofiles
from httpx2 import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .shared.database import db
from .shared.models import Unit


async def get_model(
    name: str,
    client: AsyncClient,
    sem: asyncio.Semaphore
) -> bytes:
    async with sem:
        resp = await client.get(f"https://cdn.modelviewer.lol/extras/models/{name}_ue/0/model.glb")
        resp.raise_for_status()
        return resp.content


async def create_binary_file(
    model: bytes,
    name: str
) -> None:
    async with aiofiles.open(f"/opt/game_data/shared/models_3d/{name}.glb", 'wb') as f:
        await f.write(model)


async def main(
    session: AsyncSession
) -> None:

    sem = asyncio.Semaphore(15)

    names = (await session.scalars(
        select(Unit.id)
    )).all()

    if names is None:
        pass

    names_lower = [name.lower() for name in names]

    to_change = ["gromp", "raptor", "kogmaw", "nidalee"]

    for index, name in enumerate(names_lower):
        for word in to_change:
            if word in name:
                names_lower[index] = f"da_18_{word}"
        if "small" in name:
            names_lower[index] = name.replace("small", "")

    print(len(names_lower))

    async with AsyncClient(timeout=10) as client:
        models = await asyncio.gather(
            *(get_model(name, client, sem)
              for name in names_lower)
        )

    await asyncio.gather(
         *(create_binary_file(model, name)
           for model, name in zip(models, names_lower))
    )

    async with aiofiles.open("/opt/game_data/shared/models_3d/model_list.txt", 'w') as f:
        for name in names_lower:
            await f.write(f"{name}.glb\n")

async def run() -> None:
    async with db.async_session_factory() as session:
        await main(session)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e: #noqa BLE001
        print(f"\033[31mERROR\033[0m: {e}", file=sys.stderr)
        sys.exit(1)