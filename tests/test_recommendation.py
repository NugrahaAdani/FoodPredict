import os
import tempfile
import unittest
from unittest.mock import patch

from backend.services.recommendation import (
    GeminiRecommendationService,
    build_fallback_recommendation,
)
from backend.settings import load_env_file


class RecommendationTests(unittest.TestCase):
    def test_load_env_file_reads_root_style_dotenv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = os.path.join(temp_dir, ".env")
            with open(env_path, "w", encoding="utf-8") as env_file:
                env_file.write("GEMINI_API_KEY=test-key\n")
                env_file.write("GEMINI_MODEL=gemini-test\n")

            with patch.dict(os.environ, {}, clear=True):
                load_env_file(env_path)

                self.assertEqual(os.getenv("GEMINI_API_KEY"), "test-key")
                self.assertEqual(os.getenv("GEMINI_MODEL"), "gemini-test")

    def test_build_fallback_recommendation_returns_frontend_ready_payload(self):
        result = build_fallback_recommendation("bawang putih")

        self.assertEqual(result["source"], "fallback")
        self.assertIn("bawang putih", result["text"].lower())

    @patch("backend.services.recommendation.genai")
    def test_generate_returns_fallback_when_api_key_missing(self, mocked_genai):
        with patch.dict(os.environ, {}, clear=True):
            service = GeminiRecommendationService(api_key=None)

            result = service.generate("bawang putih")

            self.assertEqual(result["source"], "fallback")
            self.assertIn("bawang putih", result["text"].lower())
            mocked_genai.Client.assert_not_called()


if __name__ == "__main__":
    unittest.main()
