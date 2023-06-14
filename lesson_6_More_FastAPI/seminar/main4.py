"""
Напишите API для управления списком задач. Для этого создайте модель Task
со следующими полями:
    ○ id: int (первичный ключ)
    ○ title: str (название задачи)
    ○ description: str (описание задачи)
    ○ done: bool (статус выполнения задачи)
-------------------------------------------------------------------
API должно поддерживать следующие операции:
    ○ Получение списка всех задач: GET /tasks/
    ○ Получение информации о конкретной задаче: GET /tasks/{task_id}/
    ○ Создание новой задачи: POST /tasks/
    ○ Обновление информации о задаче: PUT /tasks/{task_id}/
    ○ Удаление задачи: DELETE /tasks/{task_id}/
Для валидации данных используйте параметры Field модели Task.
Для работы с базой данных используйте SQLAlchemy и модуль databases.
"""
import random
from typing import List
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field
import uvicorn
import sqlalchemy
import databases

DATABASE_URL = "sqlite:///seminar_6_4.db"
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('title', sqlalchemy.String(32)),
    sqlalchemy.Column('description', sqlalchemy.String(250)),
    sqlalchemy.Column('done', sqlalchemy.Boolean),
)

metadata.create_all(engine)


class Task(BaseModel):
    id: int = Field(default=None)
    title: str = Field(max_length=32)
    description: str = Field(default=None, max_length=250)
    done: bool = Field(default=False)


class TaskIn(BaseModel):
    title: str = Field(max_length=32)
    description: str = Field(default=None, max_length=250)
    done: bool = Field(default=False)


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def root():
    return {"message": "Tasks API"}


# @app.get('/fake_tasks/{count}')
# async def fake_tasks(count: int = Path(..., ge=1)):
#     for i in range(count):
#         query = tasks.insert().values(
#             title=f'task{i}',
#             description=f'Do something {i // 2}',
#             done=random.choice([True, False])
#         )
#         await database.execute(query)
#     return {'message': f'{count} tasks were created successfully!'}


@app.get('/tasks/', response_model=List[Task])
async def get_all_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get('/tasks/{task_id}/', response_model=Task)
async def get_task(task_id: int = Path(..., ge=1, le=15)):
    query = tasks.select().where(tasks.c.id == task_id)
    return await database.fetch_one(query)


@app.post('/tasks/', response_model=Task)
async def create_task(task: TaskIn):
    query = tasks.insert().values(
        title=task.title,
        description=task.description,
        done=task.done
    )
    new_task_id = await database.execute(query)
    return {**task.dict(), 'id': new_task_id}


@app.put('/tasks/{task_id}/', response_model=Task)
async def edit_task(new_task: TaskIn, task_id: int = Path(..., ge=1)):
    query = tasks.update().where(tasks.c.id == task_id).values(**new_task.dict())
    await database.execute(query)
    return {**new_task.dict(), 'id': task_id}


@app.delete('/tasks/{task_id}/')
async def delete_task(task_id: int = Path(..., ge=1)):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {'message': f'Task with id {task_id} was deleted!'}


if __name__ == '__main__':
    uvicorn.run('main4:app', host='127.0.0.1', port=8000, reload=True)
