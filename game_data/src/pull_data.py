import asyncio
import json
import sys
from typing import Any

import aiofiles
from httpx2 import AsyncClient

paths = [
    "https://api-hc.metatft.com/tft-stat-api/units",
    "https://api-hc.metatft.com/tft-stat-api/items_matches",
    "https://api-hc.metatft.com/tft-stat-api/traits",
    "https://api-hc.metatft.com/tft-stat-api/augments_tiers",
]

async def fetch_data(
    client: AsyncClient,
    path: str
) -> dict[str, Any]:
    resp = await client.get(path)
    resp.raise_for_status()

    return resp.json()


async def  create_file(
    filename: str,
    dict: dict[str, Any]
) -> None:

    content = json.dumps(dict, indent=2)

    async with aiofiles.open(filename, 'w') as f:
        await f.write(content)


async def main() -> None:
    async with AsyncClient(timeout=10) as client:
        dicts = await asyncio.gather(
            *(fetch_data(client, path)
              for path in paths)
        )

    filenames = [path.replace("https://api-hc.metatft.com/tft-stat-api/", "") for path in paths]

    await asyncio.gather(
        *(create_file("/opt/game_data/" + filename + ".json", dict)
          for filename, dict in zip(filenames, dicts))
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e: #noqa BLE001
        print(f"\033[31mERROR\033[0m: {e}", file=sys.stderr)
        sys.exit(1)