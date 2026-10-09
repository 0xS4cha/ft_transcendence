from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

USERNAME_PATTERN = r"^[A-Za-z0-9_-]{3,32}$"

Username = Annotated[str, StringConstraints(pattern=USERNAME_PATTERN)]

from backend_app.core.validators import SafeString


class UserCreate(BaseModel):
    email: EmailStr
    username: Username
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords don't match")
        return self


class   UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: SafeString
    picture: SafeString | None = None


class   UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    picture: str | None = None
