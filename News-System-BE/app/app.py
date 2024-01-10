from flask import Flask
from routers.news import news_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    app.register_blueprint(news_blueprint,url_prefix = "/news")

    return app