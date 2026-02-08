from locust import HttpUser, task, between
import random


class NewsUser(HttpUser):
    wait_time = between(1, 5)
    article_ids = []

    def on_start(self):
        """
        Called when a User starts running.
        We'll fetch some initial articles to populate our ID list so we can read them later.
        """
        self.fetch_initial_articles()

    def fetch_initial_articles(self):
        """Helper to get article IDs from the common articles endpoint."""
        try:
            with self.client.get(
                "/news/common-articles?skip=0",
                name="/news/common-articles (init)",
                catch_response=True,
            ) as response:
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        self.article_ids.extend(
                            [item["_id"] for item in data if "_id" in item]
                        )
                else:
                    response.failure(
                        f"Failed to fetch initial articles: {response.status_code}"
                    )
        except Exception as e:
            print(f"Error fetching initial articles: {e}")

    @task(3)
    def view_common_articles(self):
        """Simulate viewing the list of common articles with pagination."""
        # Randomize skip to simulate scrolling
        skip = random.choice([0, 9, 18, 27])
        with self.client.get(
            f"/news/common-articles?skip={skip}", name="/news/common-articles"
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        # Add new IDs to our list for reading later
                        new_ids = [item["_id"] for item in data if "_id" in item]
                        # Keep list size manageable (last 100 items)
                        self.article_ids = (self.article_ids + new_ids)[-100:]
                except Exception:
                    pass

    @task(2)
    def view_latest_news(self):
        """Simulate checking the latest news."""
        with self.client.get("/news/lastest", name="/news/lastest") as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict) and "_id" in data:
                        self.article_ids.append(data["_id"])
                except Exception:
                    pass

    @task(5)
    def read_article(self):
        """Simulate reading a specific article."""
        if not self.article_ids:
            self.fetch_initial_articles()

        if self.article_ids:
            article_id = random.choice(self.article_ids)
            self.client.get(f"/news/{article_id}", name="/news/[id]")

    @task(1)
    def search_articles(self):
        """Simulate searching for articles."""
        keywords = [
            "technology",
            "business",
            "health",
            "science",
            "sports",
            "world",
            "finance",
            "bitcoin",
        ]
        query = random.choice(keywords)
        self.client.get(f"/news/search?q={query}&skip=0", name="/news/search")
