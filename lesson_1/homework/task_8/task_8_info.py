"""
Создать базовый шаблон для всего сайта, содержащий
общие элементы дизайна (шапка, меню, подвал), и
дочерние шаблоны для каждой отдельной страницы.
Например, создать страницу "О нас" и "Контакты",
используя базовый шаблон.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    context = {'title': 'Main'}
    return render_template('index8.html', **context)


@app.route('/contacts/')
def contacts():
    context = [
        {'title': 'Contacts'},
        {'address': 'Azeroth, Kalimdor, Durotar, Orgrimmar 24'},
        {'phone': '+375(29)-123-45-67'},
        {'email': 'loctarogar@duromail.ork'},
    ]
    return render_template('contacts8.html', context=context)


@app.route('/about/')
def about():
    context = {'title': 'About us'}
    return render_template('about_us8.html', **context)


if __name__ == '__main__':
    app.run()
