import pymongo
from pymongo import MongoClient
from bson import ObjectId
from flask import jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")
    nltk.download("punkt")


class MongoService:
    def __init__(self, url, database_name):
        self.client = MongoClient(url)
        self.db = self.client[database_name]
        self.collection = self.db["news"]
        self.stop_words = set(stopwords.words("english"))

    def _format_doc(self, doc):
        """Hàm hỗ trợ convert ObjectId sang string."""
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def find(self, query, exclude=None, skip=0, limit=9):
        docs = list(self.collection.find(query, exclude).skip(skip).limit(limit))
        return jsonify([self._format_doc(doc) for doc in docs])

    def find_one(self, query):
        doc = self.collection.find_one(query)
        if not doc:
            return jsonify({"error": "Not found"}), 404
        return jsonify(self._format_doc(doc))

    def find_lastest_news(self):
        doc = self.collection.find().sort("publishedAt", pymongo.DESCENDING).limit(1)
        results = list(doc)
        return jsonify(self._format_doc(results[0])) if results else jsonify({})

    def search_article(self, q, skip=0, limit=9):
        word_tokens = word_tokenize(q)
        tokens = [
            w for w in word_tokens if w.lower() not in self.stop_words and len(w) > 1
        ]

        if not tokens:
            return jsonify([])

        regex_pattern = "|".join(map(re.escape, tokens))
        query = {"title": {"$regex": regex_pattern, "$options": "i"}}

        docs = list(self.collection.find(query).skip(skip).limit(limit))
        return jsonify([self._format_doc(doc) for doc in docs])
