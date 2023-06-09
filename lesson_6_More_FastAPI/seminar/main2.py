"""
Создать веб-приложение на FastAPI, которое будет предоставлять API для
работы с базой данных пользователей. Пользователь должен иметь
следующие поля:
    ○ ID (автоматически генерируется при создании пользователя)
    ○ Имя (строка, не менее 2 символов)
    ○ Фамилия (строка, не менее 2 символов)
    ○ Дата рождения (строка в формате "YYYY-MM-DD")
    ○ Email (строка, валидный email)
    ○ Адрес (строка, не менее 5 символов)
-------------------------------------------------------------------------
API должен поддерживать следующие операции:
    ○ Добавление пользователя в базу данных
    ○ Получение списка всех пользователей в базе данных
    ○ Получение пользователя по ID
    ○ Обновление пользователя по ID
    ○ Удаление пользователя по ID
Приложение должно использовать базу данных SQLite3 для хранения пользователей.
"""
from datetime import datetime
from typing import List
from fastapi.params import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field
import databases
import uvicorn
import sqlalchemy

DATABASE_URL = "sqlite:///seminar_6_2.db"
database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("surname", sqlalchemy.String(50)),
    sqlalchemy.Column("date_of_birth", sqlalchemy.String(30)),
    sqlalchemy.Column("email", sqlalchemy.String(50)),
    sqlalchemy.Column("address", sqlalchemy.String(120)),
)

metadata.create_all(engine)


class User(BaseModel):
    id: int = Field(default=None, alias='user_id')
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    date_of_birth: str = Field(description='date in format YYYY-MM-DD')
    email: str = Field(min_length=4, max_length=50)
    address: str = Field(min_length=5, max_length=120)


class UserIn(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    date_of_birth: str = Field(description='date in format YYYY-MM-DD')
    email: str = Field(regex=r'(\w+)[@]{1}(\w+)[.]{1}(\w+)')
    address: str = Field(min_length=5, max_length=120)


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/')
async def root():
    return {'message': 'Hello, mates!'}


# @app.get('/fake_users/{count}')
# async def fake_users(count: int):
#     for i in range(count):
#         query = users.insert().values(
#             name=f'Name{i}',
#             surname=f'Surname{i ** 2}',
#             date_of_birth=f'{datetime.strptime("2000-01-24", "%Y-%m-%d").date() + timedelta(days=i ** 2)}',
#             email=f'Email{i}{i}{i}@mail.btr',
#             address=f'Mexico, Mexico, Chvalla {i}-{i * i}'
#         )
#         await database.execute(query)
#     return {'message': f'{count} fake users created and db inserted'}


@app.get('/users/', response_model=List[User])
async def get_all_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}')
async def get_user(user_id: int = Path(..., title="User id to get", ge=1)):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post('/users/{user_id}', response_model=User)
async def add_user(user: UserIn):
    query = users.insert().values(
        name=user.name,
        surname=user.surname,
        date_of_birth=datetime.strptime(user.date_of_birth, '%Y-%m-%d').date(),
        email=user.email,
        address=user.address,
    )
    add_id = await database.execute(query)
    return {**user.dict(), 'id': add_id}


@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), 'id': user_id}


@app.delete('/users/{user_id}')
async def delete_user(user_id: int = Path(..., title='User ID to delete', ge=1)):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': f'User with id {user_id} was deleted'}


if __name__ == '__main__':
    uvicorn.run("main2:app", host='127.0.0.1', port=8000, reload=True)
