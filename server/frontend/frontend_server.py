from hashlib import sha512
from sqlalchemy.exc import IntegrityError
from threading import Thread

import requests
from flask_login import LoginManager, login_user
from flask import Flask, jsonify, render_template, redirect
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest

from databases import create_session
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from models import UserORM, Post
from joke.joke_api import get_joke
from flask import request


app = Flask(f'{__name__}.frontend')
app.config['SECRET_KEY'] = 'yalms'

login_manager = LoginManager()
login_manager.init_app(app)

BACKEND_IP = 'http://localhost:8080'


@login_manager.user_loader
def load_user(username):
    db_session = create_session()
    user_select = select(UserORM).where(UserORM.username == username)
    return db_session.execute(user_select).scalar()


@app.route('/status', methods=['GET'])
def index():
    return 'frontend-server is running', 200


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": "BAD_REQUEST", "detail": e.get_description()}), 400


def start_frontend_server() -> Thread:
    frontend_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8000})
    frontend_thread.start()
    # print('http://0.0.0.0:8000')
    return frontend_thread


@app.route('/')
def start_menu():
    try:
        joke_text = get_joke()
    except Exception:
        joke_text = "Сегодня шутка отдыхает. Попробуйте позже"
    return render_template('start_screen.html', joke_text=joke_text)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        database_sess: Session = create_session()
        user_select = select(UserORM).where(or_(UserORM.email == form.username.data,
                                                UserORM.username == form.username.data))
        user: UserORM = database_sess.execute(user_select).scalar()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/posts')
        return render_template('login.html', form=form,
                               login_error='Неверное имя пользователя или пароль')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        database_sess: Session = create_session()
        try:
            hashed_password = sha512(form.password.data.encode('utf-8'), usedforsecurity=True).hexdigest()
            user = UserORM(
                name=form.fullname.data,
                username=form.username.data,
                email=form.email.data,
                hashed_password=hashed_password,
            )
            database_sess.add(user)
            database_sess.commit()
            login_user(user)
            return redirect('/posts')

        except IntegrityError:
            database_sess.rollback()
            return render_template('register.html', form=form,
                                   register_error='Пользователь с таким именем или email уже существует')
        finally:
            database_sess.close()

    return render_template('register.html', form=form)


@app.route('/policy')
def policy():
    return render_template('policy.html')


@app.route('/posts')
def posts():
    response = requests.get(f'{BACKEND_IP}/posts')
    print(f'{BACKEND_IP}/posts')
    print(response.status_code)
    posts_list = [Post.model_validate(p) for p in response.json()]
    return render_template('main_posts.html',
                           posts=[post.to_html_compatible() for post in posts_list])


@app.route('/main')
def main_():
    username = "Алексей"
    bio = "Разработчик и дизайнер. Люблю создавать красивые интерфейсы."
    user_posts = [
        {
            'image_path': 'static/images/icon.png',
            'caption': 'Мой первый пост в KeepTouch!',
            'author': 'alex_dev'
        }
    ]
    return render_template(
        'main.html',
        username=username,
        bio=bio,
        posts_count=len(user_posts),
        user_posts=user_posts
    )


@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        image = request.files['image']
        caption = request.form.get('caption', '').strip()
        return render_template('main.html')

    return render_template('create_post.html')
