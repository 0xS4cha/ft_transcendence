from pydantic import BaseModel


class Augment(BaseModel):
    id: str
    name: str
    rarity: str
    rounds: list[str]
    icon: str