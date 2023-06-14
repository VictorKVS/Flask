"""
1)Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
содержать следующие поля:
    ○ Имя пользователя (обязательное поле)
    ○ Электронная почта (обязательное поле, с валидацией на корректность ввода email)
    ○ Пароль (обязательное поле, с валидацией на минимальную длину пароля)
    ○ Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
2) После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
заполнено или данные не прошли валидацию, то должно выводиться соответствующее
сообщение об ошибке.
3) Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
об ошибке.
"""
from flask import Flask, render_template, request
import secrets
from flask_wtf.csrf import CSRFProtect
from task_4_forms import RegistrationForm
from task_4_models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
app.config['SECRET_KEY'] = secrets.token_hex()
db.init_app(app)
csrf = CSRFProtect(app)


@app.route('/')
def index():
    context = {'title': 'Website main page'}
    return render_template('index.html', **context)


@app.cli.command('init-db')
def init():
    db.create_all()
    print('OK')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        username = form.name.data
        email = form.email.data
        password = form.password.data

        new_user = User(user_name=username, email=email, password=password)
        check_user = db.session.query(User).filter(User.email == f'{email}' and User.user_name == f'{username}').all()
        print(new_user)
        print(check_user)
        if not check_user:
            db.session.add(new_user)
            db.session.commit()
            return f'<h1>{new_user.user_name} register successful!</h1>'
        return f'<h1>User {new_user.user_name} already exists!</h1>'
    context = {'title': 'Registration'}
    return render_template('register.html', form=form, **context)


@app.route('/users/')
def all_users():
    users = User.query.all()
    context = {'title': 'Students', 'users': users}
    return render_template('users.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
