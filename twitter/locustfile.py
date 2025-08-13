"""
Integrated load testing scenarios
File that integrates all load testing patterns
"""
from locust import HttpUser, task, between
import random
import string


def create_user_login():
    """Common user0001-0100 random login functionality"""

    def register_and_login(self):
        # Random selection from user0001-0100
        user_number = random.randint(1, 100)
        self.username = f"user{user_number:04d}"
        self.email = f"{self.username}@test.com"
        self.password = "password123"

        # Login attempt
        response = self.client.post("/login", data={
            "mailaddress": self.email,
            "password": self.password
        }, catch_response=True)

        if response.status_code != 302:
            # Register if user doesn't exist
            self.client.post("/register", data={
                "name": self.username,
                "mailaddress": self.email,
                "password": self.password
            })
    return register_and_login


class RealisticUser(HttpUser):
    """Realistic user behavior scenario"""
    wait_time = between(3, 10)  # Interval close to real users
    weight = 3  # Basic usage pattern

    def on_start(self):
        self.register_and_login()
        self.session_tweet_count = 0
        self.max_tweets_per_session = random.randint(3, 15)

    register_and_login = create_user_login()

    @task(10)
    def browse_timeline(self):
        """Browse timeline (most common action)"""
        self.client.get("/timeline")

    @task(5)
    def check_trends(self):
        """Check trends"""
        self.client.get("/")

    @task(3)
    def post_tweet_conditionally(self):
        """Conditional tweet posting (with session limit)"""
        if self.session_tweet_count < self.max_tweets_per_session:
            realistic_tweets = [
                "Good morning! Let's do our best today",
                "Lunch time! What should I eat?",
                "Work is over, thank you for your hard work",
                "The movie I saw today was very good",
                "Let's make plans for the weekend",
                "It was fun meeting with friends",
                "Learning new technology is fun",
                "Coffee is delicious",
            ]
            tweet_content = random.choice(realistic_tweets)
            self.client.post("/tweet", data={"msg": tweet_content})
            self.session_tweet_count += 1

    @task(2)
    def search_content(self):
        """Content search"""
        search_terms = ["today", "fun", "delicious", "movie", "music", "travel"]
        query = random.choice(search_terms)
        self.client.get(f"/search?q={query}")

    @task(2)
    def view_own_profile(self):
        """View own profile"""
        user_id = random.randint(1, 5)
        self.client.get(f"/user/{user_id}")

    @task(1)
    def check_favorites(self):
        """Check favorites"""
        self.client.get("/favorites")

    @task(1)
    def social_interactions(self):
        """Social interactions (like, follow)"""
        action = random.choice(['favorite', 'follow'])
        if action == 'favorite':
            tweet_id = random.randint(1, 50)
            self.client.post(f"/favorite/{tweet_id}")
        else:
            user_id = random.randint(1, 10)
            self.client.post(f"/follow/{user_id}")


class LurkerUser(HttpUser):
    """Lurker (read-only) user behavior pattern"""
    wait_time = between(5, 15)
    weight = 4  # Many read-only users in real SNS

    def on_start(self):
        self.register_and_login()

    register_and_login = create_user_login()

    @task(8)
    def browse_timeline(self):
        """Browse timeline"""
        self.client.get("/timeline")

    @task(3)
    def check_trends(self):
        """Check trends"""
        self.client.get("/")

    @task(2)
    def browse_profiles(self):
        """Browse other users' profiles"""
        user_id = random.randint(1, 10)
        self.client.get(f"/user/{user_id}")

    @task(1)
    def search_content(self):
        """Occasional search"""
        search_terms = ["news", "technology", "hobby", "movie", "book"]
        query = random.choice(search_terms)
        self.client.get(f"/search?q={query}")


class APIStressUser(HttpUser):
    """API intensive load test user"""
    wait_time = between(0.1, 0.5)  # High load with short intervals
    weight = 1  # Small number for load testing

    def on_start(self):
        self.register_and_login()

    register_and_login = create_user_login()

    @task(5)
    def rapid_tweet_posting(self):
        """API load test with continuous tweet posting"""
        tweet_content = f"API stress test #{random.randint(1, 10000)}"
        self.client.post("/tweet", data={"msg": tweet_content})

    @task(3)
    def rapid_favorite_actions(self):
        """Continuous favorite actions"""
        tweet_id = random.randint(1, 100)
        self.client.post(f"/favorite/{tweet_id}")

    @task(2)
    def rapid_follow_actions(self):
        """Continuous follow actions"""
        user_id = random.randint(1, 20)
        self.client.post(f"/follow/{user_id}")

    @task(1)
    def rapid_unfavorite_actions(self):
        """Continuous unfavorite actions"""
        tweet_id = random.randint(1, 100)
        self.client.post(f"/unfavorite/{tweet_id}")

    @task(1)
    def rapid_unfollow_actions(self):
        """Continuous unfollow actions"""
        user_id = random.randint(1, 20)
        self.client.post(f"/unfollow/{user_id}")


class DatabaseStressUser(HttpUser):
    """Database load test user"""
    wait_time = between(0.5, 2)
    weight = 1  # Small number for load testing

    def on_start(self):
        self.register_and_login()

    register_and_login = create_user_login()

    @task(3)
    def complex_search_queries(self):
        """Apply DB load with complex search queries"""
        # Multi-character search (DB load with LIKE clause)
        search_terms = [
            "a", "i", "u", "e", "o",  # Single character search with many hits
            "test", "system", "performance", "database"
        ]
        query = random.choice(search_terms)
        self.client.get(f"/search?q={query}")

    @task(2)
    def load_user_profiles_extensively(self):
        """Mass user profile loading"""
        # Load multiple user profiles consecutively
        for _ in range(random.randint(3, 7)):
            user_id = random.randint(1, 100)
            self.client.get(f"/user/{user_id}")

    @task(2)
    def mass_tweet_creation(self):
        """Mass tweet creation"""
        # Post multiple tweets in short time
        for i in range(random.randint(2, 5)):
            tweet_content = f"DB stress test tweet #{i} {
                random.randint(
                    1, 10000)}"
            self.client.post("/tweet", data={"msg": tweet_content})

    @task(2)
    def social_graph_operations(self):
        """Social graph operations (follow relationship CRUD)"""
        # Repeat follow/unfollow for DB write load
        user_id = random.randint(1, 50)
        self.client.post(f"/follow/{user_id}")
        # Wait a bit then unfollow
        self.client.post(f"/unfollow/{user_id}")

    @task(1)
    def favorites_heavy_operations(self):
        """Heavy favorites operations"""
        # Repeat like/unlike operations
        for _ in range(random.randint(5, 10)):
            tweet_id = random.randint(1, 200)
            self.client.post(f"/favorite/{tweet_id}")
            if random.choice([True, False]):
                self.client.post(f"/unfavorite/{tweet_id}")

    @task(1)
    def load_relationship_data(self):
        """Mass relationship data loading"""
        # Heavy JOIN queries for follower/following list display
        self.client.get("/followers")
        self.client.get("/following")
        self.client.get("/favorites")


class AnonymousUser(HttpUser):
    """Simulate anonymous user behavior"""
    wait_time = between(2, 5)
    weight = 1  # Lower frequency than TwitterUser

    @task(3)
    def view_trends(self):
        """View trends (anonymous user)"""
        self.client.get("/")

    @task(1)
    def try_login(self):
        """Login attempt"""
        self.client.get("/login")
