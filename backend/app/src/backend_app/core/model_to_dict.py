from typing import Any
from sqlalchemy import inspect

def model_to_dict(
        obj
) -> dict[str, Any]:
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
