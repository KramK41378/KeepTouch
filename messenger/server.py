from typing import List

from setup import setup, Config
from flask import Flask, request


class Server:
    app = Flask(__name__)

    def __init__(self):
        self.config: Config = setup()
        self.name: str = self.config.name
        self.messages: List[str] = []

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
        return self.messages

    @app.route('/send_message', methods=['POST'])
    def send_message(self):
        ...