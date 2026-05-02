from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

tasks = []


class Task(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class TaskResponse(Task):
    id: int


@app.get("/tasks/", response_model=List[TaskResponse])
def get_tasks():
    return [{"id": idx, **task} for idx, task in enumerate(tasks)]

@app.get("/tasks/{task_id}/", response_model=TaskResponse)
def get_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return {"id": task_id, **tasks[task_id]}

@app.post(
    "/tasks/", response_model=dict, status_code=status.HTTP_201_CREATED
)
def create_task(task: Task):
    task_data = task.model_dump()
    tasks.append(task_data)
    return {"status": "Task added", "task_id": len(tasks) - 1}

@app.put("/tasks/{task_id}/", response_model=dict)
def update_task(task_id: int, updated_task: Task):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    tasks[task_id] = updated_task.model_dump()
    return {"status": "Task updated", "task_id": task_id}

@app.delete("/tasks/{task_id}/", response_model=dict)
def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    del tasks[task_id]
    return {"status": "Task deleted"}