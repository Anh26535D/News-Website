import os
from flask import Blueprint, request, abort
from bson import ObjectId
from app.service.mongo import MongoService

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:21017")
DB_NAME = os.environ.get("DB_NAME", "news_db")

news_blueprint = Blueprint("news", __name__)
mongo_service = MongoService(url=MONGO_URI, database_name=DB_NAME)


def get_pagination_params():
    try:
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 9))
        return skip, limit
    except ValueError:
        return 0, 9


@news_blueprint.route("/common-articles", methods=["GET"])
def get_common_articles():
    skip, limit = get_pagination_params()
    query = {"urlToImage": {"$ne": ""}}
    return mongo_service.find(query, skip=skip, limit=limit)


@news_blueprint.route("/<id>", methods=["GET"])
def get_articles(id):
    if not ObjectId.is_valid(id):
        abort(400, description="Invalid ID format")
    return mongo_service.find_one({"_id": ObjectId(id)})


@news_blueprint.route("/lastest", methods=["GET"])
def get_lastest():
    return mongo_service.find_lastest_news()


@news_blueprint.route("/search", methods=["GET"])
def search_article():
    q = request.args.get("q", "")
    skip, limit = get_pagination_params()
    if not q:
        return mongo_service.find({}, skip=skip, limit=limit)
    return mongo_service.search_article(q, skip, limit)
