from fastapi import FastAPI, Depends, HTTPException, Path, status
from typing import Annotated, Any
from pydantic import BaseModel, Field 
from sqlalchemy.orm import Session # type: ignore
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
async def read_all_todos(db: db_dependency):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_new_todo(db: db_dependency, todo_request: TodosRequest):
    
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()

@app.put("/todo/{todo_id}")
async def update_todo(db: db_dependency, todo_id : int,todo_request: TodosRequest):
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@app.delete("/todo/{todo_id}")
async def delete_todo(db: db_dependency, todo_id: int):
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.delete(todo_model)
    db.commit()