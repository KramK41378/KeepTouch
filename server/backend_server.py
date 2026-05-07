from threading import Thread

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return 'backend-server is running'


from werkzeug.exceptions import BadRequest


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": "BAD_REQUEST", "detail": e.get_description()}), 400


def startup() -> Thread:
    backend_thread = Thread(target=app.run, daemon=True, kwargs={'host': '0.0.0.0', 'port': 8080})
    backend_thread.start()
    return backend_thread
