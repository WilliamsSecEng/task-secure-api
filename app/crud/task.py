from sqlalchemy.orm import Session
from app.models.task import Task

def create_task(db: Session, title: str, owner_id: int):
    task = Task(title=title, owner_id=owner_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int):
    return db.get(Task, task_id)

def get_tasks_for_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.owner_id == user_id).all()

def get_all_tasks(db: Session):
    return db.query(Task).all()

def update_task(db: Session, task: Task, data: dict):
    for key, value in data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()