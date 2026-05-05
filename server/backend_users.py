from hashlib import sha512

from flask import jsonify, request
from sqlalchemy import select, Select

from databases import create_session
from models import UserORM, User
from .backend_server import app


def get_users_by_query(query: Select) -> list[User]:
    with create_session() as session:
        raw_users = session.execute(query).scalars()
    users: list[User] = [User.from_custom_orm(user) for user in raw_users]
    return users


@app.route('/users', methods=['GET'])
def get_users():  # -> list[User]
    query = select(UserORM).order_by(UserORM.username)

    users: list[User] = get_users_by_query(query)

    return jsonify(users)


@app.route('/users/<string:username>', methods=['GET'])
def get_user(username: str):  # -> User
    query = select(UserORM).where(UserORM.username == username)

    user: User = get_users_by_query(query)[0]

    return jsonify(user)


@app.route('/check_user_password', methods=['POST'])
def check_user_password():
    username: str = request.json.get('username')
    password: str = request.json.get('password')
    hashed_password: str = sha512(password.encode('utf-8'), usedforsecurity=True).hexdigest()
    user: User = User.model_validate(get_user(username).json)
    return hashed_password == user.hashed_password


@app.route('/add/user', methods=['POST'])
def add_user():
    with create_session() as session:
        try:
            user_model = User.model_validate(request.json)

            user_orm = UserORM.from_pydantic_model(user_model)

            session.add(user_orm)
            session.commit()
        except:
            session.rollback()
            return False
        return True
