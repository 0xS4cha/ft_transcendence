from pydantic import BaseModel

class Item(BaseModel):
    id: str
    name: str
    avg_place: float
    winrate: float
    frequency: float
    type: str
    composition: list[str] 
    icon: str