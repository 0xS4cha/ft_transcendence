from typing import Annotated

from pydantic import AfterValidator, StringConstraints


def reject_null_bytes(value: str) -> str:
    if "\x00" in value:
        raise ValueError("Null characters (\\x00) are not allowed.")
    return value


SafeString = Annotated[
    str,
    StringConstraints(),
    AfterValidator(reject_null_bytes),
]