from flask import Flask, jsonify, session, abort
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
  
    stmt = db.select(Article)
    articles = db.session.execute(stmt).scalars().all()
    data = [article.to_dict() for article in articles]
    return jsonify(data), 200

@app.route('/articles/<int:id>')
def show_article(id):
  
    article = db.session.get(Article, id)
    if not article:
        abort(404, description="Article not found")

    session['page_views'] = session.get('page_views', 0) + 1

    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    return jsonify(article.to_dict()), 200

if __name__ == '_main_':
    app.run(port=5555) 
