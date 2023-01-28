import sqlite3
import os
from flask import Flask, render_template, url_for, render_template, url_for, request, flash, session, redirect, abort

DATABASE = '/tmp/flsk.db'
DEBUG = True
SECRET_KEY = 'dhbyg3y2b12b4jknsdjk32u4'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsk.db')))


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()

menu = [
    {'name': "Главная", 'url': 'index'},
    {'name': "Категории", 'url': 'categories'},
    {'name': "Доставка", 'url': 'delivery'},
    {'name': "О нас", 'url': 'about'},
    {'name': "Обратная связь", 'url': 'contact'},
]


@app.route("/index")
@app.route("/")
def index():
    print(url_for('index'))
    return render_template("index.html", title='Главная', menu=menu)


@app.route("/categories")
def categories():
    return render_template("categories.html", title='Категории', menu=menu)


@app.route("/delivery")
def delivery():
    return render_template("delivery.html", title='Доставка', menu=menu)


@app.route("/about")
def about():
    return render_template('about.html', title='О нас', menu=menu)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 2:
            flash('Сообщение отправленно успешно!', category='success')
        else:
            flash('Ошибка отправки!', category='error')
    return render_template('contact.html', title='Обратная связь', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html',title='Страница не найдена', menu=menu),404


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'alex' and request.form['password'] == 'alex98':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация пользователя', menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Пользователь: {username}"


if __name__ == "__main__":
    app.run(debug=True)
