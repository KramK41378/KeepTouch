from .post import Post, PostORM
from .user import User, UserORM

User.model_rebuild()
Post.model_rebuild()
