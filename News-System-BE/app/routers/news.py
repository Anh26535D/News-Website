import os
import sys
sys.path.insert(0,'News-System-BE/app/Service')
from bson import ObjectId



MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = os.environ.get('DB_NAME')

from flask import Blueprint, request
from Service.mongo import MongoService

news_blueprint = Blueprint('news', __name__,)
mongo_service = MongoService(url=MONGO_URI,database_name=DB_NAME)

@news_blueprint.route('/common-articles',methods=['GET'])
def get_common_articles():
    params =request.args.to_dict()
    query = {
        "urlToImage": {"$ne": ""}
    }
    return mongo_service.find(query,{},int(params.get('skip')) if params.get('skip') !=None  else 0,9)

@news_blueprint.route('/<id>',methods=['GET'])
def get_articles(id):
    query = {
        "_id":ObjectId(id)
    }
    return mongo_service.find_one(query)

@news_blueprint.route('/search',methods=['GET'])
def search_article():
    query = request.args.to_dict()
    return mongo_service.search_article(query['q'],int(query.get('skip')) if query.get('skip') !=None  else 0,9)