"""
1) Создать страницу, на которой будет форма для ввода имени
и электронной почты
2) При отправке которой будет создан cookie файл с данными
пользователя
3) Также будет произведено перенаправление на страницу
приветствия, где будет отображаться имя пользователя.
4) На странице приветствия должна быть кнопка "Выйти"
5) При нажатии на кнопку будет удален cookie файл с данными
пользователя и произведено перенаправление на страницу
ввода имени и электронной почты.
"""
import secrets

from flask import Flask, render_template, request, url_for, redirect, abort, flash, make_response, session
from pathlib import PurePath, Path

from markupsafe import escape
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = secrets.token_hex()


@app.route('/')
def index():
    context = {'title': 'main'}
    return render_template('index.html', **context)


@app.route('/hello/')
def hello():
    usr = 'Dima'
    return f"Hello, {usr}!"


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
        return f"<h2>File >>{file_name}<< uploaded!</h2>"
    context = {'title': 'Upload'}
    return render_template('upload.html', **context)


@app.get('/login/')
def submit_get():
    context = {'title': 'Sign up'}
    return render_template('login.html', **context)


@app.post('/login/')
def submit_post():
    users = ['Dima', 'Tanya', 'Sasha', 'Liza']
    user_info = {
        'Dima': 'qwerty',
        'Tanya': 'asdf',
        'Sasha': '123',
        'Liza': 'lollipop'
    }
    user = request.form.get('login')
    password = request.form.get('password')
    if user in users and password == user_info[user]:
        return f"<h1>Hello, {user}</h1>"
    else:
        context = {'title': 'wrong data'}
        return render_template('401.html', **context)


@app.get('/text_form/')
def text_get():
    context = {'title': 'Texter'}
    return render_template('text.html', **context)


@app.post('/text_form/')
def text_post():
    string = escape(request.form.get('textarea'))
    words = len(string.split(' '))
    context = {
        'title': 'calculator',
        'text': string,
        'result': words
    }
    return render_template('texter_result.html', context=context)


@app.errorhandler(401)
def not_auth(e):
    app.logger.warning(e)
    context = {'title': 'Access denied'}
    return render_template(url_for('401.html'), **context), 401


@app.route('/calculator/', methods=['GET', 'POST'])
def nums_calc():
    if request.method == 'POST':
        num1 = escape(request.form.get('num1'))
        num2 = escape(request.form.get('num2'))
        try:
            num1 = int(num1)
            num2 = int(num2)
        except:
            try:
                num1 = float(num1)
                num2 = float(num2)
            except ValueError:
                return redirect(url_for('not_auth'))
        if request.form.get('option') == 'Plus':
            _sum = num1 + num2
            return f"Sum of {num1} and {num2} = {_sum}"
        elif request.form.get('option') == 'Minus':
            subt = num1 - num2
            return f"Subtraction of {num1} and {num2} = {subt}"
        elif request.form.get('option') == 'Mult':
            mult = num1 * num2
            return f"Multiplication of {num1} and {num2} = {mult}"
        elif request.form.get('option') == 'Div':
            if num2 == 0:
                return 'Infinity'
            div = num1 / num2
            return f"Division of {num1} and {num2} = {div}"
    context = {'title': 'Nums calculator'}
    return render_template('nums_calc.html', **context)


@app.route('/adults/', methods=['GET', 'POST'])
def check_age():
    if request.method == 'POST':
        name = request.form.get('username')
        age = request.form.get('age')
        if int(age) >= 18:
            return f"<h1 style='text-align: center'>Well, hello Mr.{name}!</h1><br>"
        else:
            abort(403)
    context = {'title': 'For adults'}
    return render_template('age_checker.html', **context)


@app.errorhandler(403)
def wrong_data(e):
    app.logger.warning(e)
    context = {'title': 'Not allowed'}
    return render_template('403.html', **context), 403


@app.route('/squared/', methods=['GET', 'POST'])
def square():
    context = {'title': 'squared num'}
    if request.method == 'POST':
        num = request.form.get('number')
        return f"Square value of number {num} is {int(num)**2}"
    return render_template('square_num.html', **context)


@app.route('/flash/', methods=['GET', 'POST'])
def flashed():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please, enter your name')
            return redirect(url_for('flashed'))
        name = request.form.get('name')
        flash(f'Hello {name}')
        return redirect(url_for('flashed'))
    return render_template('flash_form.html')


@app.route('/cookie_form/', methods=['GET', 'POST'])
def set_cookie():
    if request.method == 'POST':
        context = {'title': 'main', 'name': request.form.get('login')}
        name = request.form.get('login')
        response = make_response(render_template('index.html', **context))
        response.set_cookie(name, 'Python_dev')
        return response
    context = {'title': 'cookies'}
    return render_template('cookie_form.html', **context)


@app.route('/delcookie/')
def delcookie():
    context = {'title': 'cookies'}
    response = make_response(render_template('cookie_form.html', **context))
    response.set_cookie(*request.cookies, expires=0)
    return response


if __name__ == '__main__':
    app.run()
