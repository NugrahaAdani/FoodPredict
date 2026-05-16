import asyncio
import io
import unittest
from unittest.mock import patch

from fastapi import UploadFile

from backend.main import health_check, predict


class MainApiTests(unittest.TestCase):
    @patch("backend.main.generate_recommendation")
    @patch("backend.main.predict_uploaded_image")
    def test_predict_returns_frontend_ready_shape(
        self,
        mocked_predict,
        mocked_recommendation,
    ):
        mocked_predict.return_value = {
            "predicted_class": "bawang putih",
            "confidence": 0.97,
            "probabilities": {"bawang putih": 0.97, "jahe": 0.03},
        }
        mocked_recommendation.return_value = {
            "text": "Bawang putih cocok untuk tumisan dan sup.",
            "source": "gemini",
        }

        upload = UploadFile(
            filename="sample.jpg",
            file=io.BytesIO(b"fake-image"),
        )
        upload.headers = {"content-type": "image/jpeg"}

        payload = asyncio.run(predict(upload))

        self.assertEqual(payload["filename"], "sample.jpg")
        self.assertEqual(payload["prediction"]["label"], "bawang putih")
        self.assertEqual(payload["prediction"]["confidence"], 0.97)
        self.assertEqual(payload["recommendation"]["source"], "gemini")

    def test_predict_rejects_non_image_file(self):
        upload = UploadFile(
            filename="sample.txt",
            file=io.BytesIO(b"not-image"),
        )
        upload.headers = {"content-type": "text/plain"}

        with self.assertRaises(Exception) as ctx:
            asyncio.run(predict(upload))

        self.assertEqual(ctx.exception.status_code, 400)
        self.assertEqual(ctx.exception.detail, "File harus berupa gambar.")

    def test_health_check_returns_ok(self):
        self.assertEqual(health_check(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
