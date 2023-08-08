from app import db


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author = db.Column(db.String(128))
    link = db.Column(db.String(256), unique=True)
    pubdate = db.Column(db.DateTime)
    guid = db.Column(db.String(256), unique=True)

    def __repr__(self):
        return f'Title <{self.title}>, Author(s) <{self.author}>'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author = db.Column(db.String(128))
    link = db.Column(db.String(256), unique=True)
    pubdate = db.Column(db.DateTime)
    guid = db.Column(db.String(256), unique=True)

    def __repr__(self):
        return f'Title <{self.title}>, Author(s) <{self.author}>'
