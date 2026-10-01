from pydantic import BaseModel


class   UnitTrait(BaseModel):
    name: str
    breakpoints: list[str]
    icon: str
