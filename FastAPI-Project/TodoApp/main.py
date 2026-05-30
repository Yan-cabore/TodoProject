from fastapi import FastAPI, Depends, HTTPException, Path, status
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Todos
from database import engine, SessionLocal


app = FastAPI()

class TodosRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(max_length=100)
    priority: int = Field(ge=1, lt=6)
    complete: bool
    
    

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_id(db: db_dependency, todo_id: int = Path(gt=0)):
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todos(db: db_dependency, todo_request: TodosRequest):
    pass