from flask import Flask
from .routers.news import news_blueprint

# from .routers.track import track_blueprint
from app.service.mongo import MongoService
from app.service.seeder import NewsDataGenerator
import os


def create_app():
    fapp = Flask(__name__)
    mongo_uri = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME")
    mongo_service = MongoService(url=mongo_uri, database_name=db_name)

    @fapp.cli.command("seed")
    def seed_db():
        """Lệnh: flask seed"""
        seeder = NewsDataGenerator(
            db=mongo_service.db, newsapi_apikey=os.environ.get("NEWSAPI_APIKEY")
        )
        seeder.seed()

    fapp.register_blueprint(news_blueprint, url_prefix="/news")
    # app.register_blueprint(track_blueprint, url_prefix="/track")
    return fapp
