import feedparser
from app import app, db
from app.models import Review, Article
from flask import render_template, url_for, request
from time import mktime
from datetime import datetime, timezone


def to_datetime(entry_date):
    return datetime.fromtimestamp(mktime(entry_date), timezone.utc)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Home')


@app.route('/reviews')
def reviews():
    feeds = ['https://pitchfork.com/rss/reviews/albums/',
             'https://www.rollingstone.com/music/music-album-reviews/feed/']

    for feed in feeds:
        parsed_feed = feedparser.parse(feed)

        for entry in parsed_feed.entries:
            review_guid = Review.query.filter_by(guid=entry.id).first()

            if review_guid is None:
                new_review = Review(title=entry.title, link=entry.link, pubdate=to_datetime(
                    entry.published_parsed), guid=entry.id)
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
    feeds = ['https://pitchfork.com/rss/news/',
             'https://www.rollingstone.com/music/music-news/feed/']

    for feed in feeds:
        parsed_feed = feedparser.parse(feed)

        for entry in parsed_feed.entries:
            article_guid = Article.query.filter_by(guid=entry.id).first()

            if article_guid is None:
                new_article = Article(title=entry.title, link=entry.link, pubdate=to_datetime(
                    entry.published_parsed), guid=entry.id)
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
