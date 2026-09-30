from pydantic import BaseModel
from backend_app.schemas.unit_trait import UnitTrait

class   Unit(BaseModel):
    id: str
    name: str
    avg_place: float
    winrate: float
    frequency: float
    cost: int
    traits: list[UnitTrait] = []
    icon: str
    model: str | None
