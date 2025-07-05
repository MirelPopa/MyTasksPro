from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped
from db.main import Base

class Task(Base):
    __tablename__ = "tasks"
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)
    description = mapped_column(String)
    priority = mapped_column(Integer)
    due_date = mapped_column(DateTime)
    created_at = mapped_column(DateTime)
    completed = mapped_column(Boolean)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="tasks")

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True, index=True)
    email = mapped_column(String, unique=True, index=True)
    hashed_password = mapped_column(String)
    tasks: Mapped[Task] = relationship(back_populates="user")
