import asyncio
import sys
from typing import Any

import aiofiles
import json
from httpx2 import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .shared.database import db
from .shared.models import Unit


async def fetch_model(
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


def parse_names(
    names: list[str]
) -> list[str]:
    names_lower = [name.lower() for name in names]
    
    to_change = ["gromp", "raptor", "kogmaw", "nidalee"]

    for index, name in enumerate(names_lower):
        for word in to_change:
            if word in name:
                names_lower[index] = f"da_18_{word}"
        if "small" in name:
            names_lower[index] = name.replace("small", "")

    return names_lower


async def fetch_units(
    client: AsyncClient
) -> list[dict[str, Any]]:
    resp = await client.get(f"https://api-hc.metatft.com/tft-stat-api/units")
    resp.raise_for_status()

    return resp.json()["results"]


async def fetch_set_data(
    client: AsyncClient
) -> list[dict[str, Any]]:
    resp = await client.get("https://raw.communitydragon.org/latest/cdragon/tft/en_us.json")
    resp.raise_for_status()
    
    return next((e for e in resp.json()["setData"] if e["mutator"] == "TFTSet18"), None)    


async def main(
) -> None:
    sem = asyncio.Semaphore(15)

    async with AsyncClient(timeout=10) as client:
        units = await fetch_units(client)

    units_ids = [unit["unit"] for unit in units if "TFT" not in unit["unit"]]

    async with AsyncClient(timeout=10) as client:
        set_data = fetch_set_data(client)

    if set_data is None:
        raise ValueError("Set data for TFTSet18 not found")
    
    champions_by_id = {c["apiName"]: c for c in set_data["champions"]}

    names = [champions_by_id[id]["name"] for id in units_ids]

    names_lower = parse_names(names)

    async with AsyncClient(timeout=10) as client:
        models = await asyncio.gather(
            *(fetch_model(name, client, sem)
              for name in names_lower)
        )

    await asyncio.gather(
         *(create_binary_file(model, name)
           for model, name in zip(models, names_lower))
    )

    model_dict = {id: f"{name}.glb" for id, name in zip(units_ids, names_lower)}
    content = json.dumps(model_dict, indent=2)

    async with aiofiles.open(f"/opt/game_data/shared/models_3d/models_list.json", 'w') as f:
        await f.write(content)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e: #noqa BLE001
        print(f"\033[31mERROR\033[0m: {e}", file=sys.stderr)
        sys.exit(1)