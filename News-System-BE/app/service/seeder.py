# app/service/seeder.py
import requests
from pymongo import MongoClient
from faker import Faker


class NewsDataGenerator:
    def __init__(self, db, newsapi_apikey=None):
        self.db = db
        self.collection = self.db["news"]
        self.newsapi_apikey = newsapi_apikey
        self.fake = Faker()

    def is_empty(self):
        """Kiểm tra xem DB đã có dữ liệu chưa."""
        return self.collection.count_documents({}) == 0

    def seed(self, num_news=20):
        if not self.is_empty():
            print("--- Data already exists. Skipping seed. ---")
            return

        print("--- Database is empty. Starting seeding... ---")
        if self.newsapi_apikey:
            self._fetch_from_api()
        else:
            self._fetch_random(num_news)
        print("--- Seeding completed! ---")

    def _fetch_from_api(self):
        url = f"https://newsapi.org/v2/everything?q=technology&sortBy=popularity&apiKey={self.newsapi_apikey}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            if articles:
                self.collection.insert_many(articles)
        else:
            print(f"API Error: {response.status_code}. Falling back to random.")
            self._fetch_random(10)

    def _fetch_random(self, num):
        news = []
        for _ in range(num):
            news.append(
                {
                    "source": {"id": None, "name": self.fake.company()},
                    "author": self.fake.name(),
                    "title": self.fake.sentence(),
                    "description": self.fake.paragraph(),
                    "url": self.fake.url(),
                    "urlToImage": self.fake.image_url(),
                    "publishedAt": self.fake.date_time_this_year().isoformat() + "Z",
                    "content": self.fake.text(),
                }
            )
        self.collection.insert_many(news)
