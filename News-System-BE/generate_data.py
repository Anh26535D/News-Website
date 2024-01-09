import os
import dotenv
import requests

from pymongo import MongoClient
from faker import Faker


dotenv.load_dotenv()


mongodb_uri = os.environ.get('MONGO_URI')
newsapi_apikey = os.environ.get('NEWSAPI_APIKEY')
db_mongo_name = os.environ.get('DB_NAME')
collection_mongo_name = os.environ.get('COLLECTION_NAME')


class NewsDataGenerator:

    def __init__(self, mongodb_uri=None, newsapi_apikey=None, num_news=100) -> None:
        if mongodb_uri is None:
            raise Exception("Mongodb URI is not provided")
        self.mongodb_uri = mongodb_uri
        self.newsapi_apikey = newsapi_apikey
        self.num_news = num_news
        self.fake = Faker()

    def run(self):
        if self.newsapi_apikey is None:
            print("Start fetching data by random...")
            self.fetch_data_by_random()
            print("Done")
        else:
            print("Start fetching data from API...")
            self.fetch_data_from_api()
            print("Done")

    def fetch_data_from_api(self):
        url = f"https://newsapi.org/v2/everything?q=apple&sortBy=popularity&apiKey={newsapi_apikey}"

        client = MongoClient(mongodb_uri)
        db = client[str(db_mongo_name)]
        collection = db[str(collection_mongo_name)]

        response = requests.get(url)

        if response.status_code == 200:
            response_json = response.json()
            articles = response_json['articles']
            collection.insert_many(articles)
        else:
            raise Exception("Error when fetching data from API")
        client.close()

    def random_news(self):
        news = {
            "source": {
                "id": "", 
                "name": self.fake.company()
            }, 
            "author": self.fake.name(), 
            "title": self.fake.sentence(), 
            "description": self.fake.paragraph(), 
            "url": self.fake.url(), 
            "urlToImage": self.fake.image_url(), 
            "publishedAt": self.fake.date_time_this_decade().isoformat() + "Z",
            "content": self.fake.text()
        }

        return news

    def fetch_data_by_random(self, num_news=100):
        client = MongoClient(mongodb_uri)
        db = client[str(db_mongo_name)]
        collection = db[str(collection_mongo_name)]

        news = [self.random_news() for _ in range(num_news)]
        collection.insert_many(news)
        client.close()

data_gen = NewsDataGenerator(mongodb_uri, newsapi_apikey)
data_gen.run()