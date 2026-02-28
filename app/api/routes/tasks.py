from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.deps_auth import get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.crud.task import (
    create_task,
    get_task,
    get_tasks_for_user,
    get_all_tasks,
    update_task,
    delete_task,
)

router = APIRouter()

@router.post("/", response_model=TaskOut)
def create_new_task(data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_task(db, title=data.title, owner_id=user.id)

@router.get("/", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == "admin":
        return get_all_tasks(db)
    return get_tasks_for_user(db, user.id)

@router.get("/{task_id}", response_model=TaskOut)
def get_one_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if user.role != "admin" and task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return task

@router.patch("/{task_id}", response_model=TaskOut)
def update_one_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if user.role != "admin" and task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return update_task(db, task, data.dict(exclude_unset=True))

@router.delete("/{task_id}")
def delete_one_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if user.role != "admin" and task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    delete_task(db, task)
    return {"message": "Task deleted"}