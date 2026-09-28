from pydantic import BaseModel

class Trait(BaseModel):
    id: str
    name: str
    avg_place: float
    winrate: float
    frequency: float
    breakpoint: str
    breakpoints: list[str]
    icon: str
    background_icon: str