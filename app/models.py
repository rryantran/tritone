from app import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, unique=True)
    link = db.Column(db.String(256), index=True, unique=True)
    desc = db.Column(db.String(512))
    pubdate = db.Column(db.DateTime)

    def __repr__(self):
        return f'Title <{self.title}>, Source <{self.source}>, Date Published <{self.pubdate}>'
