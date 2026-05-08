from threading import Thread

from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(f'{__name__}.frontend')


@app.route('/')
def index():
    return 'frontend-server is running'


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": "BAD_REQUEST", "detail": e.get_description()}), 400


def start_frontend_server() -> Thread:
    frontend_thread = Thread(target=app.run, daemon=True, kwargs={'host': '0.0.0.0', 'port': 8000})
    frontend_thread.start()
    return frontend_thread
