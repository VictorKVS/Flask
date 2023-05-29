"""
1) Создать базу данных для хранения информации о книгах в библиотеке.
2) База данных должна содержать две таблицы: "Книги" и "Авторы".
3) В таблице "Книги" должны быть следующие поля: id, название, год издания,
количество экземпляров и id автора.
4) В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
5) Необходимо создать связь между таблицами "Книги" и "Авторы".
6) Написать функцию-обработчик, которая будет выводить список всех книг с
указанием их авторов.
"""
import random

from flask import Flask, render_template
from task_2_models import db, Books, Authors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seminardb.db'
db.init_app(app)


@app.route('/')
def index():
    context = {'title': 'Faculty main page'}
    return render_template('index.html', **context)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.cli.command('fill-auth')
def fill_authors():
    count = 5
    for author in range(1, count + 1):
        new_author = Authors(first_name=f'Name{author}',
                             last_name=f'Surname{author}')
        db.session.add(new_author)
    db.session.commit()
    print('Authors OK')


@app.cli.command('fill-b')
def fill_books():
    count = 5
    for book in range(1, count ** 2):
        author = Authors.query.filter_by(last_name=f'Surname{book % count + 1}').first()
        new_book = Books(name=f'Bookname{book}',
                         year=random.randint(2003, 2023),
                         amount=random.randint(10, 250),
                         author=author)
        db.session.add(new_book)
    db.session.commit()
    print('Books OK')


@app.route('/books/')
def library():
    books = Books.query.all()
    authors = Authors.query.all()
    context = {'title': 'Library', 'books': books, 'authors': authors}
    return render_template('books.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
