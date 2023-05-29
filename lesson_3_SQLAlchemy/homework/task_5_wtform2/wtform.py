"""
1) Создать форму регистрации для пользователя.
2) Форма должна содержать поля: имя, электронная почта,
пароль (с подтверждением), дата рождения, согласие на
обработку персональных данных.
3) Валидация должна проверять, что все поля заполнены
корректно (например, дата рождения должна быть в
формате дд.мм.гггг).
4) При успешной регистрации пользователь должен быть
перенаправлен на страницу подтверждения регистрации.
"""
from flask import Flask, render_template, request, redirect, url_for
import secrets
from flask_wtf.csrf import CSRFProtect
from task_5_forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()
csrf = CSRFProtect(app)


@app.route('/')
def index():
    context = {'title': 'Website main page'}
    return render_template('index.html', **context)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        return redirect(url_for('confirmation'))
    context = {'title': 'Registration'}
    return render_template('register.html', form=form, **context)


@app.route('/confirm/')
def confirmation():
    context = {'title': 'Confirmation'}
    return render_template('confirmation.html', **context)


@app.route('/cancel/')
def cancellation():
    return redirect(url_for('index'))


@app.route('/agree/')
def agreement():
    return '<h1>Registration successful!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
