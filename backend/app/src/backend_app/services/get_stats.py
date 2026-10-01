from backend_app.core.utils import safe_get


def get_all_datas_use(
        data: list
) -> int:
    total = 0

    for d in data:
        total += sum(d.get("places"), 0)

    return (total)


def get_stats(
    places: list,
    total_data_use: int,
    all_datas_use: int,
) -> tuple[float, float, float]:
    
    weighted = 0
    for rank, count in enumerate(places, start=1):
        weighted += rank * count
    weighted /= total_data_use

    winrate = (safe_get(places, 0) / total_data_use) * 100

    if all_datas_use == 0:
        frequency = 0
    else:
        frequency = (total_data_use / all_datas_use) * 100

    return weighted, winrate, frequency