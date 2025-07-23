from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Todo(BaseModel):
    id: int
    titre: str
    description: Optional[str] = None
    Terminer: bool = False

todos: List[Todo] = []

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return sorted(todos, key=lambda todo: todo.id)


@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    for t in todos:
        if t.id == todo.id:
            raise HTTPException(status_code=400, detail="Une tâche avec cet ID existe déjà")
    todos.append(todo)
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo):
    for i, t in enumerate(todos):
        if t.id == todo_id:
            todos[i] = todo
            return todo
    raise HTTPException(status_code=404, detail="Tâche non trouvée")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, t in enumerate(todos):
        if t.id == todo_id:
            todos.pop(i)
            return {"message": "Tâche supprimée"}
    raise HTTPException(status_code=404, detail="Tâche non trouvée")
