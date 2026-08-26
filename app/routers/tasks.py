from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import database dependency
from app.database import get_db

# Import schemas
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

# Import task service
from app.services import task_service

# Import current logged-in user
from app.auth import get_current_user


# Create a router for task APIs
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# Create a new task
@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.create_task(
        db,
        task_data,
        current_user.id
    )


# Get all tasks of the current user
@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return task_service.get_all_tasks(
        db,
        skip,
        limit,
        current_user.id
    )


# Get one task by ID
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = task_service.get_task_by_id(
        db,
        task_id
    )

    # Check if task exists
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Check if the task belongs to the current user
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access this task"
        )

    return task


# Update a task
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = task_service.get_task_by_id(
        db,
        task_id
    )

    # Check if task exists
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Check if the task belongs to the current user
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot update this task"
        )

    return task_service.update_task(
        db,
        task,
        task_data
    )


# Delete a task
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = task_service.get_task_by_id(
        db,
        task_id
    )

    # Check if task exists
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # Check if the task belongs to the current user
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this task"
        )

    task_service.delete_task(
        db,
        task
    )

    return {
        "message": "Task deleted successfully"
    }