from app import app
import unittest
import os
import json
os.environ['TESTING'] = 'true'


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        # Tests relating to home page:
        # assert "<title>Cyber Sapiens Home</title>" in html
        # assert "<h1 class=\"about-header\">The story of how we ended up MLH fellows</h1>" in html
        # assert "Welcome to our portfolio" in html
        # assert "Scroll through our website and witness what we've accomplished!" in html
        # assert "Cras dui velit" in html
        self.assertIsNotNone(html)

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # Tests relating to GET and POST endpoints
        post = self.client.post("/api/timeline_post", data=dict(
            {"name": "John Doe", "email": "john@example.com", "content": "Hello world, I\'m John!"}))
        assert post.status_code == 200

        response_2 = self.client.get("/api/timeline_post")
        assert response_2.status_code == 200
        assert response_2.is_json
        json = response_2.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1

        # Tests relating to timeline page
        response_3 = self.client.get("/timeline2")
        assert response_3.status_code == 200
        html = response_3.get_data(as_text=True)
        assert '<input name="name" type="text" placeholder="name" />' in html
        assert '<input name="email" type="text" placeholder="email" />' in html
        assert '<input name="content" type="text" placeholder="content" />' in html
        assert "<button type=\"submit\">Submit</button>" in html
        assert "fetch" in html
        self.assertIsNotNone(html)

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
                                    "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
