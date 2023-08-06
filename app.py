from app import app, db
from app.models import Review, Article


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Review': Review, 'Article': Article}


if __name__ == '__main__':
    app.run()
