"""
1) Создать API для управления списком задач.
2) Каждая задача должна содержать поля "название",
"описание" и "статус" (выполнена/не выполнена).
3) API должен позволять выполнять CRUD операции с
задачами.
"""
import random

from fastapi import FastAPI
from fastapi.params import Path
import uvicorn
from pydantic import BaseModel, Field
from typing import List

tasks = []

for i in range(10):
    tasks.append({'title': f'do_smth {i}',
                  'description': f'Some description {i}',
                  'status': random.choice([True, False])})

app = FastAPI()


class Tasks(BaseModel):
    title: str = Field(max_length=32)
    description: str = Field(max_length=120)
    status: bool = Field(default=False)


@app.get('/tasks/', response_model=List[Tasks])
async def get_tasks():
    return tasks


@app.get('/tasks/{task_id}', response_model=Tasks)
async def get_task(task_id: int = Path(..., ge=0, le=len(tasks))):
    return tasks[task_id]


@app.post('/tasks/', response_model=Tasks)
async def create_task(task: Tasks):
    tasks.append(task)
    return task


@app.put('/tasks/{task_id}', response_model=Tasks)
async def update_task(new_task: Tasks, task_id: int = Path(..., ge=0, le=len(tasks))):
    tasks[task_id] = new_task
    return new_task


@app.delete('/tasks/{task_id}', response_model=Tasks)
async def delete_task(task_id: int = Path(..., ge=0, le=len(tasks))):
    return tasks.pop(task_id)


if __name__ == '__main__':
    uvicorn.run("main3:app", host="127.0.0.1", port=8000, reload=True)


