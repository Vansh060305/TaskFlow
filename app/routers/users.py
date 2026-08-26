from fastapi import APIRouter, Depends, HTTPException

# Import database session type
from sqlalchemy.orm import Session

# Import database dependency
from app.database import get_db

# Import schemas
from app.schemas import UserCreate, UserUpdate, UserResponse

# Import user service
from app.services import user_service
from app.auth import get_current_user

# Create a router for user APIs
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Create a new user
@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return user_service.create_user(db, user_data)


# Get all users
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)


# Get one user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# Update a user
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user_service.update_user(db, user, user_data)


# Delete a user
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_service.get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user_service.delete_user(db, user)

    return {"message": "User deleted successfully"}