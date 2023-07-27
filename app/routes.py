import feedparser
from app import app, db
from app.models import Article
from flask import render_template
from time import mktime
from datetime import datetime, timezone


def to_datetime(entry_date):
    return datetime.fromtimestamp(mktime(entry_date), timezone.utc)


@app.route('/')
@app.route('/home')
def index():
    feeds = ['https://pitchfork.com/rss/news/']

    for feed in feeds:
        parsed_feed = feedparser.parse(feed)

        for entry in parsed_feed.entries:
            article_title = Article.query.filter_by(title=entry.title).first()

            if article_title is None:
                new_article = Article(title=entry.title, link=entry.link,
                                      desc=entry.description, pubdate=to_datetime(entry.published_parsed))
                db.session.add(new_article)
                db.session.commit()

    articles = Article.query.all()

    return render_template('index.html', title='Home', articles=articles)
