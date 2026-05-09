from threading import Thread

from flask import Flask, jsonify, render_template
from werkzeug.exceptions import BadRequest
from templates.joke.joke_api import get_joke

app = Flask(f'{__name__}.frontend')


@app.route('/status', methods=['GET'])
def index():
    return 'frontend-server is running', 200


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": "BAD_REQUEST", "detail": e.get_description()}), 400


def start_frontend_server() -> Thread:
    frontend_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8000})
    frontend_thread.start()
    print('http://0.0.0.0:8000')
    return frontend_thread


@app.route('/')
def start_menu():
    try:
        joke_text = get_joke()
    except Exception:
        joke_text = "Сегодня шутка отдыхает. Попробуйте позже"
    return render_template('Start_screen.html', joke_text=joke_text)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/posts')
def posts():
    return render_template('main_posts.html')

@app.route('/main')
def main_():
    return render_template('main.html')
