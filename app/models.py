from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'User <{self.email}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author = db.Column(db.String(128))
    link = db.Column(db.String(256), unique=True)
    pubdate = db.Column(db.DateTime)
    guid = db.Column(db.String(256), unique=True)
    source = db.Column(db.String(218))

    def __repr__(self):
        return f'Title <{self.title}>, Author <{self.author}>'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author = db.Column(db.String(128))
    link = db.Column(db.String(256), unique=True)
    pubdate = db.Column(db.DateTime)
    guid = db.Column(db.String(256), unique=True)
    source = db.Column(db.String(218))

    def __repr__(self):
        return f'Title <{self.title}>, Author <{self.author}>'
