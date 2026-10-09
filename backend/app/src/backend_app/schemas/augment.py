from pydantic import BaseModel

from backend_app.core.validators import SafeString


class Augment(BaseModel):
    id: SafeString
    name: SafeString
    rarity: SafeString
    rounds: list[SafeString]
    icon: SafeString