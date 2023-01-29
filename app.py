import random
import datetime
import os
import sqlite3

import git
from flask import Flask, render_template, flash, redirect, session, url_for, request, abort, g

from fdatabase import FDataBase
from forms import LoginForm

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

login_in_pass = {'max': '123', 'alex': '321', 'den': '0000'}

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fdb.db')))
app.permanent_session_lifetime = datetime.timedelta(seconds=60)


@app.route('/update_server', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/maxXT/s')
        origin = repo.remotes.origin
        origin.pull()
        return 'Сайт обновился', 200
    else:
        return 'Возникла ошибка', 400


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/test2')
def test2():  # put application's code here

    return f'Авторизация пользователя!'
@app.route('/test3')
def test3():  # put application's code here

    return f'Авторизация пользователя!'

@app.route('/admin/', methods=['POST', 'GET'])
def admin():  # put application's code here

    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))
    elif request.method == 'POST' and request.form['username'] not in login_in_pass:
        login_in_pass[request.form['username']] = request.form['psw']
        print(login_in_pass)
    elif request.method == 'POST' and request.form['username'] in login_in_pass:
        del login_in_pass[request.form['username']]
        print(login_in_pass)
    return render_template('admin.html', title='Авторизация пользователя')


@app.route('/login2/', methods=['POST', 'GET'])
def login2():  # put application's code here

    if 'userlogged' in session:
        return redirect(url_for('profile', username=session['userlogged']))

    elif request.method == 'POST' and request.form['username'] in login_in_pass and request.form['psw'] == \
            login_in_pass[request.form['username']]:

        session['userlogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userlogged']))
    return render_template('login_v2.html', title='Авторизация пользователя')


@app.route('/profile/<username>')
def profile(username):
    if 'userlogged' not in session or session['userlogged'] != username:
        abort(401)
    return f'<h1> Пользователь {username}'


@app.route('/post')
def post():  # put application's code here

    return render_template('post.html')


@app.route('/login/')
def login():  # put application's code here
    form = LoginForm()
    return render_template('login.html', title='Авторизация пользователя', form=form)


@app.route('/')
@app.route('/index')
def index():
    db = get_db()
    database = FDataBase(db)

    return render_template('index.html', title=str(random.randint(1, 4)), menu=database.getMenu())


# @app.route('/user/<username>')
# def user_profile(username):  # put application's code here
#   return render_template('index.html', title=str(random.randint(1, 4)))


# @app.route('/user/<int:post_id>')
# def show_post(post_id):  # put application's code here
#    return f"<h1>Горячая и свежая новость № {post_id}</h1>"

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page404.html", title="Страница не найдена")


if __name__ == '__main__':
    app.run(debug=True)
