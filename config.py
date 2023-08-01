import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or f'sqlite:///{os.path.join(basedir, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10
