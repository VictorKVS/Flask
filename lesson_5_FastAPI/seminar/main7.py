"""
Создать RESTful API для управления списком задач. Приложение должно
использовать FastAPI и поддерживать следующие функции:
    ○ Получение списка всех задач.
    ○ Получение информации о задаче по её ID.
    ○ Добавление новой задачи.
    ○ Обновление информации о задаче по её ID.
    ○ Удаление задачи по её ID.
Каждая задача должна содержать следующие поля: ID (целое число),
Название (строка), Описание (строка), Статус (строка):
todo, in progress, done.
----------------------------------------------------------------------------
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс Task с полями id, title, description и status.
Создайте список tasks для хранения задач.
Создайте функцию get_tasks для получения списка всех задач (метод GET).
Создайте функцию get_task для получения информации о задаче по её ID
(метод GET).
Создайте функцию create_task для добавления новой задачи (метод POST).
Создайте функцию update_task для обновления информации о задаче по её ID
(метод PUT).
Создайте функцию delete_task для удаления задачи по её ID (метод DELETE).
"""
from random import choice
from fastapi import FastAPI, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int = Field(default=None)
    title: str = Field(min_length=2, max_length=50)
    description: str = Field(max_length=200)
    status: str


tasks = []
for i in range(1, 21):
    task = Task(id=i,
                title=f'Title{i}',
                description='Some description',
                status=f'{choice(["todo", "in progress", "done"])}')
    tasks.append(task)

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/')
async def root():
    return {'message': 'Task #7'}


@app.get('/tasks/', response_class=HTMLResponse)
async def get_tasks(request: Request):
    return templates.TemplateResponse('main7_template.html', {'request': request, 'tasks': tasks, 'title': 'Tasks'})


@app.get('/tasks/{task_id}', response_model=Task)
async def get_task(task_id: int = Path(..., ge=1, le=len(tasks))):
    for task in tasks:
        if task.id == task_id:
            return task


@app.post('/tasks/', response_model=Task)
async def create_task(new_task: Task):
    new_task.id = len(tasks) + 1
    tasks.append(new_task)
    return new_task


@app.put('/tasks/{task_id}', response_model=Task)
async def update_task(new_task: Task, task_id: int = Path(..., ge=1, le=len(tasks))):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            new_task.id = task_id
            tasks[idx] = new_task
            return new_task


@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int = Path(..., ge=1, le=len(tasks))):
    tasks.pop(task_id - 1)
    return {'message': f'Task with id {task_id} was deleted'}


if __name__ == '__main__':
    uvicorn.run('main7:app', host='127.0.0.1', port=8000, reload=True)
