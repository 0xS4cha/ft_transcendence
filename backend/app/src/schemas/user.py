from    pydantic    import  BaseModel, EmailStr

class   UserCreate(BaseModel):
    email: EmailStr
    password: str

class   UserPublic(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True