from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


user_article = db.Table('user_article', db.Column('user_id', db.Integer, db.ForeignKey(
    'user.id')), db.Column('article_id', db.Integer, db.ForeignKey('article.id')))

user_review = db.Table('user_review', db.Column('user_id', db.Integer, db.ForeignKey(
    'user.id')), db.Column('review_id', db.Integer, db.ForeignKey('review.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    articles = db.relationship(
        'Article', secondary=user_article, back_populates='bookmarkers')
    reviews = db.relationship(
        'Review', secondary=user_review, back_populates='bookmarkers')

    def __repr__(self):
        return f'User <{self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def bookmark_article(self, article):
        if article not in self.articles:
            self.articles.append(article)

    def unbookmark_article(self, article):
        if article in self.articles:
            self.articles.remove(article)

    def bookmark_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)

    def unbookmark_review(self, review):
        if review in self.reviews:
            self.reviews.remove(review)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    link = db.Column(db.String(256), unique=True)
    pubdate = db.Column(db.DateTime, index=True)
    guid = db.Column(db.String(256), index=True, unique=True)
    source = db.Column(db.String(218))
    bookmarkers = db.relationship(
        'User', secondary=user_review, back_populates='reviews')

    def __repr__(self):
        return f'Title <{self.title}>, Author <{self.author}>'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    link = db.Column(db.String(256), unique=True)
    pubdate = db.Column(db.DateTime, index=True)
    guid = db.Column(db.String(256), index=True, unique=True)
    source = db.Column(db.String(218))
    bookmarkers = db.relationship(
        'User', secondary=user_article, back_populates='articles')

    def __repr__(self):
        return f'Title <{self.title}>, Author <{self.author}>'
