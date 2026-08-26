from pydantic import BaseModel


# Schema for creating a new user
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# Schema for updating a user
class UserUpdate(BaseModel):
    name: str
    email: str
    password: str


# Schema for sending user data in the response
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    # Allow Pydantic to read data from SQLAlchemy objects
    class Config:
        from_attributes = True


# Schema for creating a new task
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "pending"


# Schema for updating a task
class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    status: str


# Schema for sending task data in the response
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    user_id: int

    # Allow Pydantic to read data from SQLAlchemy objects
    class Config:
        from_attributes = True
