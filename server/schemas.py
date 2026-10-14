from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


class EmailStatusResponse(BaseModel):
    id: int
    status: str
    attempts: int
    error_message: str | None

    model_config = ConfigDict(from_attributes=True)