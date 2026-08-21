# Import the Task database model
from app.models import Task


# Create a new task
def create_task(db, task_data):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        user_id=task_data.user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# Get all tasks
def get_all_tasks(db, skip=0, limit=10):
    return db.query(Task).offset(skip).limit(limit).all()


# Get one task by ID
def get_task_by_id(db, task_id):
    return db.query(Task).filter(Task.id == task_id).first()


# Update an existing task
def update_task(db, task, task_data):
    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status

    db.commit()
    db.refresh(task)

    return task


# Delete a task
def delete_task(db, task):
    db.delete(task)
    db.commit()