from pydantic import BaseModel

from backend_app.core.validators import SafeString
from backend_app.schemas.unit_trait import UnitTrait


class   Unit(BaseModel):
    id: SafeString
    name: SafeString
    avg_place: float
    winrate: float
    frequency: float
    cost: int
    traits: list[UnitTrait] = []
    icon: SafeString
    model: SafeString | None
