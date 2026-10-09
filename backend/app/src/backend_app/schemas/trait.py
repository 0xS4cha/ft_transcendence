from pydantic import BaseModel

from backend_app.core.validators import SafeString


class Trait(BaseModel):
    id: SafeString
    name: SafeString
    avg_place: float
    winrate: float
    frequency: float
    breakpoint: SafeString
    breakpoints: list[SafeString]
    icon: SafeString
    background_icon: SafeString