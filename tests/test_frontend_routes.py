import unittest

from fastapi.testclient import TestClient

from backend.main import app


class FrontendRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_serves_frontend_html(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("Food Prediction", response.text)


if __name__ == "__main__":
    unittest.main()
