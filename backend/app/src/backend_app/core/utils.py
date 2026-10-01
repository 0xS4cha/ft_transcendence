def safe_get[T](
    lst: list[T],
    index: int,
    default: T | None = None
) -> T | None:
    return lst[index] if 0 <= index < len(lst) else default