from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True  # Updated to Pydantic V2

class UserInDB(UserBase):
    hashed_password: str

    class Config:
        from_attributes = True  # Updated to Pydantic V2
