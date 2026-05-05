from flask import Flask, jsonify
from sqlalchemy import select

from databases import create_session
from models import User, Post, UserORM, PostORM

app = Flask(__name__)

@app.route('/')
def index():
    return 'backend-server is running'

@app.route('/users', methods=['GET'])
def get_users(): # list[User]
    query = select(UserORM).order_by(UserORM.username)
    session = create_session()
    raw_users = session.execute(query).scalars()
    users: list[User] = [User.from_custom_orm(user) for user in raw_users]
    return jsonify(users)

@app.route('/posts', methods=['GET'])
def get_posts(): # list[Post]
    query = select(PostORM).order_by(PostORM.timestamp)
    session = create_session()
    raw_posts = session.execute(query).scalars()
    posts: list[Post] = [Post.from_custom_orm(post) for post in raw_posts]
    return jsonify(posts)
