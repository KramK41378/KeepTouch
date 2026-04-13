from typing import List

from pydantic import ValidationError

from messenger.message_handler import MessageHandler
from models import Message
from setup import setup, Config
from flask import Flask, request


class Server:
    app = Flask(__name__)

    def __init__(self):
        self.config: Config = setup()
        self.name: str = self.config.name
        self.message_handler: MessageHandler = MessageHandler()

    def check_client(self, name: str) -> bool:
        return name == self.name

    @app.route('/')
    def index(self):
        return 'Mars server is running'

    @app.route('/get_messages')
    def get_messages(self):
        name = request.args.get('name')
        if not self.check_client(name):
            return 'Access denied', 403
        return self.message_handler.get_messages()

    @app.route('/send_message', methods=['POST'])
    def send_message(self):
        message_raw = request.get_json()
        try:
            message = Message.model_validate_json(message_raw)
        except ValidationError as e:
            return f'Wrong message format: {e}', 400
        self.message_handler.add_message(message)
        return 200

