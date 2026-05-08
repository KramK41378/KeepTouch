from threading import Thread

from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(f'{__name__}.backend')


@app.route('/')
def index():
    return 'backend-server is running'


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": "BAD_REQUEST", "detail": e.get_description()}), 400


def start_backend_server() -> Thread:
    backend_thread = Thread(target=app.run, daemon=True, kwargs={'port': 8080})
    backend_thread.start()
    return backend_thread
