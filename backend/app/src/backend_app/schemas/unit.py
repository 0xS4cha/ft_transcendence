from pydantic import BaseModel
from backend_app.schemas.trait import Trait

class   Unit(BaseModel):
    id: str
    name: str
    avg_place: float
    winrate: float
    frequency: float
    cost: int
    traits: list[Trait] = []
    icon: str
    model: str
