# Import password hashing tools
from passlib.context import CryptContext


# Create a password hashing object
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Hash a plain password
def hash_password(password: str):
    return pwd_context.hash(password)


# Check a password against its hashed version
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)