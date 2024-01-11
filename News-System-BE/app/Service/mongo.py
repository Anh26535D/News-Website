import re

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from flask import jsonify
import pymongo
from pymongo import MongoClient



class MongoService():
    def __init__(self, url, database_name) -> None:
        self.url = url
        self.database_name = database_name

    def get_list_collections(self):
        with MongoClient(self.url) as client:
            db = client[self.database_name]
            results = db.list_collection_names()
        return results

    def insert_new(self, new):
        with MongoClient(self.url) as client:
            db = client[self.database_name]
            new_id = list(db['news'].insert_one(new))
        return new_id

    def insert_news(self, news):
        with MongoClient(self.url) as client:
            db = client[self.database_name]
            new_ids = list(db['news'].insert_many(news))
        return new_ids

    def find(self, query, exclude, skip, limit):
        with MongoClient(self.url) as client:
            db = client[self.database_name]
            news = list(db['news'].find(
                query, exclude).skip(skip).limit(limit))
            data = []
            for doc in news:
                doc['_id'] = str(doc['_id'])
                data.append(doc)
        return jsonify(data)

    def find_one(self, query):
        with MongoClient(self.url) as client:
            db = client[self.database_name]
            new = db['news'].find_one(query)
            new['_id'] = str(new['_id'])
        return jsonify(new)

    def find_lastest_news(self):
        with MongoClient(self.url) as client:
            db = client[self.database_name]
            new = db['news'].find({}, {}).sort(
                "publishedAt", pymongo.DESCENDING).limit(1)[0]
            new['_id'] = str(new['_id'])
        return jsonify(new)

    def search_article(self, q, skip, limit):
        with MongoClient(self.url) as client:
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(q)
            tokens = [w for w in word_tokens if w.lower(
            ) not in stop_words and len(w) > 1]

            regex_pattern = "|".join(map(re.escape, tokens))
            query = {"title": {"$regex": regex_pattern, "$options": "i"}}
            db = client[self.database_name]
            news = list(db['news'].find(query, {}).skip(skip).limit(limit))
            data = []
            for doc in news:
                doc['_id'] = str(doc['_id'])
                data.append(doc)
        return jsonify(data)
