from flask import jsonify, request
from pydantic import ValidationError
from sqlalchemy import select, Select
from sqlalchemy.exc import IntegrityError

from databases import create_session
from models import PostORM, Post
from .backend_server import app


def get_posts_by_query(query: Select) -> list[Post]:
    """Получает посты по запросу Select"""
    # создаем сессию базы данных
    with create_session() as session:
        # выполняем запрос
        raw_posts = session.execute(query).scalars().all()

        # преобразовываем в pydantic-модели
        posts: list[Post] = [Post.from_custom_orm(post).model_dump(mode='json') for post in raw_posts]

    # возвращаем список постов
    return posts


@app.route('/posts')
def get_posts():  # list[Post]
    """Получить все посты"""

    # создаём запрос
    query = select(PostORM).order_by(PostORM.created_at.desc())

    # выполняем запрос
    posts: list[Post] = get_posts_by_query(query)

    # преобразовываем в json и возвращаем
    return jsonify(posts)


@app.route('/posts/<int:post_id>')
def get_post_by_id(post_id: int):
    """Получить посты по id"""

    # создаём запрос
    query = select(PostORM).where(PostORM.id == post_id).order_by(PostORM.created_at)

    # выполняем запрос
    post: Post = get_posts_by_query(query)[0]

    # преобразовываем в json и возвращаем
    return jsonify(post)


@app.route('/posts/by/<string:author>', methods=['GET'])
def get_posts_by_author(author: str):
    """Получить посты по автору"""

    # создаём запрос
    query = select(PostORM).where(PostORM.author_username == author).order_by(PostORM.created_at.desc())

    # выполняем запрос
    posts: list[Post] = get_posts_by_query(query)

    # преобразовываем в json и возвращаем
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
    """
    Функция для добавления поста
    """

    # получаем данные из запроса
    data = request.get_json()

    # создаем сессию
    session = create_session()

    # используем обработчик ошибок
    try:
        # создаем объект
        post_orm = PostORM(
            text=data['text'],
            image=data['image'],
            author_username=data['author_username'],
        )

        # добавляем объект
        session.add(post_orm)

        # сохраняем в БД
        session.commit()

        # преобразовываем в json
        resp = jsonify({'id': post_orm.id, 'location': f'/posts/{post_orm.id}'})

        # ставим status code created
        resp.status_code = 201

        # возвращаем
        return resp

    # при ошибке
    except Exception as e:
        # откатываем изменения
        session.rollback()

        # возвращаем ошибку
        return jsonify({'error': 'INTERNAL', 'detail': str(e)}), 500

    # в самом конце
    finally:
        #закрываем сессию
        session.close()
