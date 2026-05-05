from threading import Thread

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'backend-server is running'

def startup() -> Thread:
    backend_thread = Thread(target=app.run, daemon=True, kwargs={'host': '0.0.0.0', 'port': 8080})
    backend_thread.start()
    return backend_thread
