from pydantic import BaseModel

from backend_app.core.validators import SafeString


class   UnitTrait(BaseModel):
    name: SafeString
    breakpoints: list[SafeString]
    icon: SafeString
