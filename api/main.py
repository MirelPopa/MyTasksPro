from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from auth.auth import create_access_token, get_current_user
from db.main import get_db, Base, engine
from db.models import User, Task
from api.schemas import Token, UserOut, UserCreate, CreateTask
from auth.password_utils import hash_password, verify_password

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
async def delete_task(item_id):
    pass

@fast_api_app.put("/tasks/{item_id}")
async def update_task(item_id):
    pass

@fast_api_app.post("/tasks/{item_id}")
async def get_task(item_id):
    pass

@fast_api_app.get("/export-status/{job_id}")
async def get_task_status(job_id):
    pass
