from pydantic import BaseModel

from backend_app.core.validators import SafeString


class Item(BaseModel):
    id: SafeString
    name: SafeString
    avg_place: float
    winrate: float
    frequency: float
    type: SafeString
    composition: list[SafeString] 
    icon: SafeString