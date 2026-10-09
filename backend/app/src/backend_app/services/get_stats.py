from typing import Any


def valid_places(places: Any) -> list[int] | None:
    if not isinstance(places, list) or not places:
        return None
    if not all(isinstance(p, int) and not isinstance(p, bool) and p >= 0 for p in places):
        return None
    return places


def get_all_datas_use(
        data: list
) -> int:
    total = 0

    for d in data:
        places = valid_places(d.get("places"))
        if places is not None:
            total += sum(places)

    return total


def get_stats(
    places: list[int],
    total_data_use: int,
    all_datas_use: int,
) -> tuple[float, float, float]:

    weighted = 0
    for rank, count in enumerate(places, start=1):
        weighted += rank * count
    weighted /= total_data_use

    winrate = (places[0] / total_data_use) * 100

    if all_datas_use == 0:
        frequency = 0
    else:
        frequency = (total_data_use / all_datas_use) * 100

    return weighted, winrate, frequency
