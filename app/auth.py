import os

# Import environment variable loader
from dotenv import load_dotenv

# Import JWT tools
from jose import jwt

# Import FastAPI dependency tools
from fastapi import Depends, HTTPException

# Import OAuth2 token reader
from fastapi.security import OAuth2PasswordBearer

# Import database session
from sqlalchemy.orm import Session

# Import database dependency
from app.database import get_db

# Import User model
from app.models import User


# Load variables from the .env file
load_dotenv()


# Get the secret key from the .env file
SECRET_KEY = os.getenv("SECRET_KEY")

# Algorithm used for JWT
ALGORITHM = "HS256"


# Tell FastAPI where users get their login token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# Create a JWT token
def create_access_token(data: dict):
    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# Get the current logged-in user
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        # Decode and verify the JWT token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get the user ID from the token
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        # Find the user in the database
        user = db.query(User).filter(
            User.id == int(user_id)
        ).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )