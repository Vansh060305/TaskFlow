from app.models import User
from app.security import hash_password


# Create a new user
def create_user(db, user_data):
    hashed_password = hash_password(user_data.password)

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get all users
def get_all_users(db):
    return db.query(User).all()


# Get one user by ID
def get_user_by_id(db, user_id):
    return db.query(User).filter(User.id == user_id).first()


# Update an existing user
def update_user(db, user, user_data):
    user.name = user_data.name
    user.email = user_data.email
    user.password = user_data.password

    db.commit()
    db.refresh(user)

    return user


# Delete a user
def delete_user(db, user):
    db.delete(user)
    db.commit()