import feedparser
from app import app, db
from app.models import Article
from flask import render_template, request
from time import mktime
from datetime import datetime, timezone


def to_datetime(entry_date):
    return datetime.fromtimestamp(mktime(entry_date), timezone.utc)


@app.route('/')
@app.route('/home')
def index():
    feeds = ['https://pitchfork.com/rss/news/', 'https://www.nme.com/news/music/feed',
             'https://i-d.vice.com/en_uk/rss/topic/music', 'https://www.rollingstone.com/music/music-news/feed/']

    for feed in feeds:
        parsed_feed = feedparser.parse(feed)

        for entry in parsed_feed.entries:
            article_title = Article.query.filter_by(title=entry.title).first()

            if article_title is None:
                new_article = Article(title=entry.title, link=entry.link,
                                      desc=entry.description, pubdate=to_datetime(entry.published_parsed))
                db.session.add(new_article)
                db.session.commit()

    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.pubdate.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False).items

    return render_template('index.html', title='Home', articles=articles)
