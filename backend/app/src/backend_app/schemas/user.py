from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from backend_app.core.validators import SafeString


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=32)
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
    id: int
    username: SafeString
    picture: SafeString | None = None

    class Config:
        from_attributes = True