import unittest

import app as legacy_app_module
import model_utils as legacy_model_utils
from backend.main import app as backend_app
from backend.services.predict import LABEL_PATH, MODEL_PATH


class LegacyModuleTests(unittest.TestCase):
    def test_legacy_app_exposes_backend_app(self):
        self.assertIs(legacy_app_module.app, backend_app)

    def test_legacy_model_utils_defaults_point_to_backend_assets(self):
        self.assertEqual(legacy_model_utils.DEFAULT_MODEL_PATH, MODEL_PATH)
        self.assertEqual(legacy_model_utils.DEFAULT_LABEL_PATH, LABEL_PATH)


if __name__ == "__main__":
    unittest.main()
