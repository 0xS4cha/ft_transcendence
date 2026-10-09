from pydantic import BaseModel, EmailStr

from backend_app.core.validators import SafeString


class   UserCreate(BaseModel):
    email: EmailStr
    username: SafeString
    password: SafeString
    confirm_password: SafeString

class   UserPublic(BaseModel):
    id: int
    email: EmailStr
    username: SafeString
    picture: SafeString | None = None

    class Config:
        from_attributes = True