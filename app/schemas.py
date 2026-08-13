from pydantic import BaseModel

class UserCreate(BaseModel):
    name : str
    email : str
    password : str

class UserResponse(BaseModel):
    id : int
    name : str
    email: str

class UserUpdate(BaseModel):
    name: str
    email: str


# ==========Task CRUD

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = "pending"
    user_id: int


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    user_id: int


class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    status: str
