from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import users, tasks , auth


# Create the FastAPI application
app = FastAPI(
    title="TaskFlow API",
    description="A simple task management backend API",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Connect user routes to the main application
app.include_router(users.router)

# Connect task routes to the main application
app.include_router(tasks.router)
# Connect auth routes to the main application
app.include_router(auth.router)


# Basic home route
@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow API"
    }



