from fastapi import APIRouter, Depends, HTTPException

# Import database session type
from sqlalchemy.orm import Session

# Import database dependency
from app.database import get_db

# Import schemas
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

# Import task service
from app.services import task_service


# Create a router for task APIs
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# Create a new task
@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    return task_service.create_task(db, task_data)


# Get all tasks
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return task_service.get_all_tasks(db, skip, limit)


# Get one task by ID
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = task_service.get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# Update a task
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = task_service.get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task_service.update_task(db, task, task_data)


# Delete a task
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = task_service.get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task_service.delete_task(db, task)

    return {"message": "Task deleted successfully"}