from flask import Flask
from sqlalchemy import select

from databases import create_session
from models import User

app = Flask(__name__)

@app.route('/')
def index():
    return 'backend-server is running'

@app.route('/users', methods=['GET'])
def get_users():
    query = select(User).order_by(User.username)
    session = create_session()
    result = session.execute(query).scalars()
    return result

@app.route('/posts', methods=['GET'])
def get_posts():