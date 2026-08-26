# Import FastAPI tools
from fastapi import APIRouter, Depends, HTTPException

# Import database session
from sqlalchemy.orm import Session

# Import OAuth2 form
from fastapi.security import OAuth2PasswordRequestForm

# Import database dependency
from app.database import get_db

# Import User model
from app.models import User

# Import schemas
from app.schemas import UserResponse

# Import password verification
from app.security import verify_password

# Import authentication functions
from app.auth import create_access_token, get_current_user


# Create an authentication router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Login user and return JWT token
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Find the user by email
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    # Check if the user exists
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check the password
    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create a JWT token
    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Get the currently logged-in user
@router.get("/me", response_model=UserResponse)
def get_me(
    current_user = Depends(get_current_user)
):
    return current_user