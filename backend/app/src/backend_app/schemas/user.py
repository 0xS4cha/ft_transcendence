from pydantic import BaseModel, EmailStr


class   UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str

class   UserPublic(BaseModel):
    id: int
    email: EmailStr
    username: str
    picture: str | None = None

    class Config:
        from_attributes = True