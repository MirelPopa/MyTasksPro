from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import select
from auth.auth import create_access_token, get_current_user
from db.main import get_db, Base, engine
from db.models import User, Task
from api.schemas import Token, UserCreate, CreateTask, TaskUpdate
from auth.password_utils import hash_password, verify_password
from worker.main import export_tasks_to_csv

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield

fast_api_app = FastAPI(lifespan=lifespan)

@fast_api_app.post("/signup", response_model=Token)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(user.email == User.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already in use")

    hashed_password = hash_password(user.password)
    new_user = User(email = user.email, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@fast_api_app.post("/login", response_model=Token)
async def log_in(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(user.email == User.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@fast_api_app.get("/me")
async def get_current_user_route(user_data: User = Depends(get_current_user)):
    return {"user_id": user_data.id,
            "user_email": user_data.email}

@fast_api_app.get("/tasks/")
async def get_tasks(user_data: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = select(Task).where(Task.user_id == user_data.id)
    result = db.execute(stmt)
    tasks = result.scalars().all()
    return tasks

@fast_api_app.post("/tasks/")
async def create_task(task: CreateTask, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_task = Task(**task.model_dump(), user_id=user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"task_id": new_task.id}

@fast_api_app.delete("/tasks/{item_id}")
async def delete_task(item_id, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = select(Task).where(Task.user_id == user.id, Task.id == item_id)
    result = db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {item_id} not found")
    db.delete(task)
    db.commit()

    return f"Deleted task {item_id}"

@fast_api_app.get("/tasks/export-tasks")
async def export_tasks_as_csv(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = select(Task).where(Task.user_id == user.id)
    result = db.execute(stmt)
    tasks = result.scalars().all()
    tasks_json = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "completed": task.completed
        }
        for task in tasks
    ]
    export_tasks_to_csv.delay(tasks_json, user.id)

@fast_api_app.get("/tasks/{item_id}")
async def get_task(item_id, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = select(Task).where(Task.user_id == user.id, Task.id == item_id)
    result = db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {item_id} not found")
    else:
        return task

@fast_api_app.put("/tasks/{item_id}")
async def update_task(item_id, task_update: TaskUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = select(Task).where(Task.user_id == user.id, Task.id == item_id)
    result = db.execute(stmt)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {item_id} not found")
    else:
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return f"Task {item_id} updated successfully!"

# @fast_api_app.get("/tasks/fuck-you/{item_id}")
# async def export_task_as_json(item_id, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     stmt = select(Task).where(Task.user_id == user.id, Task.id == item_id)
#     result = db.execute(stmt)
#     task = result.scalar_one_or_none()
#     if not task:
#         raise HTTPException(status_code=404, detail=f"Task with id {item_id} not found")
#
#     task_data = {
#         "id": task.id,
#         "title": task.title,
#         "description": task.description,
#         "priority": task.priority,
#         "due_date": task.due_date,
#         "created_at": task.created_at.isoformat() if task.created_at else None,
#         "completed": task.completed
#     }
#
#     export_task_to_json.delay(task_data)

@fast_api_app.get("/export-status/{job_id}")
async def get_task_status(job_id):
    pass
