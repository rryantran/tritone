import feedparser
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Review, Article
from flask import render_template, url_for, request, redirect
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlparse
from time import mktime
from datetime import datetime, timezone


def to_datetime(entry_date):
    return datetime.fromtimestamp(mktime(entry_date), timezone.utc)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/reviews')
def reviews():
    feeds = ['https://pitchfork.com/rss/reviews/albums/',
             'https://www.rollingstone.com/music/music-album-reviews/feed/', 'https://www.nme.com/reviews/album/feed']

    for feed in feeds:
        parsed_feed = feedparser.parse(feed)

        for entry in parsed_feed.entries:
            review_guid = Review.query.filter_by(guid=entry.id).first()

            if review_guid is None:
                source = urlparse(parsed_feed.feed.link).netloc
                if source[0:4] != 'www.':
                    source = 'www.' + source

                new_review = Review(title=entry.title, author=entry.author, link=entry.link, pubdate=to_datetime(
                    entry.published_parsed), guid=entry.id, source=source)

                db.session.add(new_review)
                db.session.commit()

    page = request.args.get('page', 1, type=int)
    reviews = Review.query.order_by(Review.pubdate.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for(
        'reviews', page=reviews.next_num) if reviews.has_next else None
    prev_url = url_for(
        'reviews', page=reviews.prev_num) if reviews.has_prev else None

    return render_template('reviews.html', title='Reviews', reviews=reviews.items, next_url=next_url, prev_url=prev_url)


@app.route('/news')
def news():
    feeds = ['https://pitchfork.com/rss/news/', 'https://www.rollingstone.com/music/music-news/feed/',
             'https://www.billboard.com/c/music/music-news/feed/', 'https://www.nme.com/news/music/feed']

    for feed in feeds:
        parsed_feed = feedparser.parse(feed)

        for entry in parsed_feed.entries:
            article_guid = Article.query.filter_by(guid=entry.id).first()

            if article_guid is None:
                source = urlparse(parsed_feed.feed.link).netloc
                if source[0:4] != 'www.':
                    source = 'www.' + source

                new_article = Article(title=entry.title, author=entry.author, link=entry.link, pubdate=to_datetime(
                    entry.published_parsed), guid=entry.id, source=source)

                db.session.add(new_article)
                db.session.commit()

    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.pubdate.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for(
        'news', page=articles.next_num) if articles.has_next else None
    prev_url = url_for(
        'news', page=articles.prev_num) if articles.has_prev else None

    return render_template('news.html', title='News', articles=articles.items, next_url=next_url, prev_url=prev_url)


@app.route('/about')
def about():
    return render_template('about.html', title='About')
