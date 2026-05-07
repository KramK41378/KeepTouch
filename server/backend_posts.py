from flask import jsonify, request
from sqlalchemy import select, Select

from databases import create_session
from models import PostORM, Post
from .backend_server import app


def get_posts_by_query(query: Select) -> list[Post]:
    with create_session() as session:
        raw_posts = session.execute(query).scalars()
    posts: list[Post] = [Post.from_custom_orm(post) for post in raw_posts]
    return posts


@app.route('/get_posts', methods=['GET'])
def get_posts():  # list[Post]
    query = select(PostORM).order_by(PostORM.timestamp)

    posts: list[Post] = get_posts_by_query(query)

    return jsonify(posts)


@app.route('/get_post/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id: int):
    query = select(PostORM).where(PostORM.id == post_id).order_by(PostORM.timestamp)

    post: Post = get_posts_by_query(query)[0]

    return jsonify(post)


@app.route('/get_posts/<string:author>', methods=['GET'])
def get_posts_by_author(author: str):
    query = select(PostORM).where(PostORM.author == author).order_by(PostORM.timestamp)

    posts: list[Post] = get_posts_by_query(query)

    return jsonify(posts)


# Временное решение, надо улучшить !!!
@app.route('/add_post', methods=['POST'])
def add_post():
    post_model = Post.model_validate_json(request.json)

    post_orm = PostORM.from_pydantic_model(post_model)

    session = create_session()
    session.add(post_orm)
    session.commit()

    return True
