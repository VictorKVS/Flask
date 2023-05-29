"""
1) Доработаем задача про студентов
2) Создать базу данных для хранения информации о студентах и их оценках в
учебном заведении.
3) База данных должна содержать две таблицы: "Студенты" и "Оценки".
4) В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, группа
и email.
5) В таблице "Оценки" должны быть следующие поля: id, id студента, название
предмета и оценка.
6) Необходимо создать связь между таблицами "Студенты" и "Оценки".
7) Написать функцию-обработчик, которая будет выводить список всех
студентов с указанием их оценок.

"""
import random

from flask import Flask, render_template
from task_3_models import db, Student, Mark

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studmarks.db'
db.init_app(app)


@app.route('/')
def index():
    context = {'title': 'Faculty main page'}
    return render_template('index.html', **context)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.cli.command('fill-stud')
def fill_students():
    count = 5
    for student in range(1, count ** 2):
        new_student = Student(
            first_name=f'name{student}',
            last_name=f'surname{student}',
            email=f'email{student}@testmail.by',
            group=random.randint(1, 5)
            )
        db.session.add(new_student)
    db.session.commit()
    print('Students filled!')


@app.cli.command('fill-mark')
def fill_marks():
    count = 10
    for grade in range(1, count ** 2):
        student = Student.query.filter_by(last_name=f'surname{grade % count + 1}').first()
        new_grade = Mark(subject=f'subject{grade}', mark=random.randint(1, 10), student=student)
        db.session.add(new_grade)
    db.session.commit()
    print('Marks filled!')


@app.route('/students/')
def all_students():
    students = Student.query.all()
    marks = Mark.query.all()
    context = {'title': 'Students', 'students': students, 'marks': marks}
    return render_template('students.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
