"""
Разработать API для управления списком пользователей с
использованием базы данных SQLite. Для этого создайте
модель User со следующими полями:
    ○ id: int (идентификатор пользователя, генерируется
    автоматически)
    ○ username: str (имя пользователя)
    ○ email: str (электронная почта пользователя)
    ○ password: str (пароль пользователя)
------------------------------------------------------------------
API должно поддерживать следующие операции:
    ○ Получение списка всех пользователей: GET /users/
    ○ Получение информации о конкретном пользователе: GET /users/{user_id}/
    ○ Создание нового пользователя: POST /users/
    ○ Обновление информации о пользователе: PUT /users/{user_id}/
    ○ Удаление пользователя: DELETE /users/{user_id}/
Для валидации данных используйте параметры Field модели User.
Для работы с базой данных используйте SQLAlchemy и модуль databases.
"""
from typing import List

import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

# pip install sqlalchemy
# pip install "uvicorn[standard]" optional

DATABASE_URL = "sqlite:///seminar_6.db"
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users",
                         metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("username", sqlalchemy.String(50)),
                         sqlalchemy.Column("email", sqlalchemy.String(120)),
                         sqlalchemy.Column("password", sqlalchemy.String(32)),
                         )

metadata.create_all(engine)


class UserIn(BaseModel):
    username: str = Field(max_length=50)
    email: str = Field(max_length=120)
    password: str = Field(max_length=32)


class User(BaseModel):
    id: int = Field(default=None, alias='user_id')
    username: str = Field(max_length=50)
    email: str = Field(max_length=120)
    password: str = Field(max_length=32)


app = FastAPI(title='DiVo DATABASE')


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def root():
    return {"message": "index"}


@app.get('/fake_users/{count}')
async def create_users(count: int):
    for i in range(count):
        query = users.insert().values(username=f'user{i}',
                                      email=f'email{i}@mail.ru',
                                      password=f'qwerty{i}')
        await database.execute(query)
    return {'message': f'{count} fake users was created and inserted into db'}


@app.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post('/users/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(
        username=user.username,
        email=user.email,
        password=user.password
        )
    actual_id = await database.execute(query)
    return {**user.dict(), 'id': actual_id}


@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), 'id': user_id}


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': f'User with id {user_id} was deleted'}


uvicorn.run(app, host="127.0.0.1", port=8000)
