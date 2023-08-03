import feedparser
from app import app, db
from app.models import Review
from flask import render_template, url_for, request
from time import mktime
from datetime import datetime, timezone


def to_datetime(entry_date):
    return datetime.fromtimestamp(mktime(entry_date), timezone.utc)


@app.route('/')
@app.route('/home')
def index():
    feeds = ['https://pitchfork.com/rss/reviews/albums/', 'https://www.rollingstone.com/music/music-album-reviews/feed/']

    for feed in feeds:
        parsed_feed = feedparser.parse(feed)

        for entry in parsed_feed.entries:
            review_title = Review.query.filter_by(title=entry.title).first()

            if review_title is None:
                new_review = Review(title=entry.title, link=entry.link, pubdate=to_datetime(
                    entry.published_parsed), guid=entry.id)
                db.session.add(new_review)
                db.session.commit()

    page = request.args.get('page', 1, type=int)
    reviews = Review.query.order_by(Review.pubdate.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for(
        'index', page=reviews.next_num) if reviews.next_num else None
    prev_url = url_for(
        'index', page=reviews.prev_num) if reviews.prev_num else None

    return render_template('index.html', title='Home', reviews=reviews.items, next_url=next_url, prev_url=prev_url)
