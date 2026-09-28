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
) -> dict[str, Any] | None:
    resp = await client.get("https://api-hc.metatft.com/tft-stat-api/units")
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
        units, set_data = await asyncio.gather(
            fetch_units(client),
            fetch_set_data(client)
        )

        if set_data is None:
            raise ValueError("Set data not found")

        units_ids = [unit["unit"] for unit in units if "TFT" not in unit["unit"]]
        
        champions_by_id = {c["apiName"]: c for c in set_data["champions"]}
        units_ids = [uid for uid in units_ids if uid in champions_by_id]
        
        names_lower = parse_names(units_ids)
    
        results = await asyncio.gather(
            *(fetch_model(name, client, sem)
              for name in names_lower),
            return_exceptions=True,
        )

    ok = []

    for uid, name, res in zip(units_ids, names_lower, results):
        if isinstance(res, BaseException):
            print(f"Failed {name}: {res}")
        else:
            ok.append((uid, name, res))

    if not ok:
        raise RuntimeError("No Models Downloaded")

    await asyncio.gather(
         *(create_binary_file(res, name)
           for _, name, res in ok)
    )

    model_dict = {uid: f"{name}.glb" for uid, name, _ in ok}
    content = json.dumps(model_dict, indent=2)

    async with aiofiles.open("/opt/game_data/shared/models_3d/models_list.json", 'w') as f:
        await f.write(content)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e: #noqa BLE001
        print(f"\033[31mERROR\033[0m: {e}", file=sys.stderr)
        sys.exit(1)