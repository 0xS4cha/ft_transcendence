from pydantic import BaseModel

class Augment(BaseModel):
    id: str
    name: str
    rarity: str
    round: list[str]
    icon: str