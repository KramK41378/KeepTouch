from threading import Thread
from pydantic import ValidationError

from messenger.message_handler import MessageHandler
from models import Message
from setup import setup, Config
from flask import Flask, request


class Server:
    def __init__(self, name: str | None = None):
        self.config: Config = setup()
        self.name: str = name or self.config.name
        self.message_handler: MessageHandler = MessageHandler()

    def check_client(self, name: str) -> bool:
        return name == self.name


server = Server()
app = Flask(__name__)
thread: Thread = Thread(target=app.run, kwargs={'port': 8080})


def run() -> None:
    thread.start()


@app.route('/')
def index():
    return 'KeepTouch server is running'


@app.route('/get_messages/<name>')
def get_messages(name):
    if not server.check_client(name):
        return 'Access denied', 403
    print(1)
    return MessageHandler.get_all_messages()


@app.route('/send_message', methods=['POST'])
def send_message():
    message_raw = request.get_json()
    try:
        message = Message.model_validate(message_raw)
    except ValidationError as e:
        return f'Wrong message format: {e}', 400
    MessageHandler.add_message(message)
    return 'Success', 200
