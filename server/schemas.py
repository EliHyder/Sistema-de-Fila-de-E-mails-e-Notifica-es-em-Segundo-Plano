from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class EmailRequest(BaseModel):
    user_id: int
    subject: str
    body: str

class EmailResponse(BaseModel):
    id: int
    user_id: int
    subject: str
    body: str
    status: str
    attempts: int
    error_message: str | None
    created_at: str
    updated_at: str | None
    class Config:
        orm_mode = True


class EmailStatusResponse(BaseModel):
    id: int
    status: str
    attempts: int
    error_message: str | None
    

    class Config:
        orm_mode = True