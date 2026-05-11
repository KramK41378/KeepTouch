from flask import jsonify, request
from pydantic import ValidationError
from sqlalchemy import select, Select
from sqlalchemy.exc import IntegrityError

from databases import create_session
from models import PostORM, Post
from .backend_server import app


def get_posts_by_query(query: Select) -> list[Post]:
    with create_session() as session:
        raw_posts = session.execute(query).scalars().all()
        posts: list[Post] = [Post.from_custom_orm(post).model_dump() for post in raw_posts]
    return posts


@app.route('/posts')
def get_posts():  # list[Post]
    query = select(PostORM).order_by(PostORM.created_at)

    posts: list[Post] = get_posts_by_query(query)

    return jsonify(posts)


@app.route('/posts/<int:post_id>')
def get_post_by_id(post_id: int):
    query = select(PostORM).where(PostORM.id == post_id).order_by(PostORM.created_at)

    post: Post = get_posts_by_query(query)[0]

    return jsonify(post)


@app.route('/posts/by/<string:author>', methods=['GET'])
def get_posts_by_author(author: str):
    query = select(PostORM).where(PostORM.author_username == author).order_by(PostORM.created_at.desc())

    posts: list[Post] = get_posts_by_query(query)

    return jsonify(posts)


# @app.route('/posts', methods=['POST'])
# def add_post():
#     raw_post_model = request.get_json()
#
#     try:
#         post_model = Post.model_validate(raw_post_model)
#     except ValidationError as e:
#         return jsonify({'error': 'validation', 'message': e.errors()}), 400
#
#     session = create_session()
#
#     try:
#         post_orm = PostORM.from_pydantic_model(post_model)
#
#         session.add(post_orm)
#         session.commit()
#
#         resp = jsonify(Post.from_custom_orm(post_orm).model_dump())
#         resp.status_code = 201
#         resp.headers['Location'] = f'/posts/{post_orm.id}'
#         return resp
#
#     except IntegrityError:
#         session.rollback()
#         return jsonify({'error': 'duplicate', 'message': 'Post with this identifier already exists'}), 409
#
#     except Exception:
#         session.rollback()
#         return jsonify({'error': 'INTERNAL', 'detail': 'Server processing error'}), 500
#
#     finally:
#         session.close()


@app.route('/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    session = create_session()
    try:
        post_orm = PostORM(
            text=data['text'],
            image=data['image'],
            author_username=data['author_username'],
        )
        session.add(post_orm)
        session.commit()
        resp = jsonify({'id': post_orm.id, 'location': f'/posts/{post_orm.id}'})
        resp.status_code = 201
        return resp
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'INTERNAL', 'detail': str(e)}), 500
    finally:
        session.close()