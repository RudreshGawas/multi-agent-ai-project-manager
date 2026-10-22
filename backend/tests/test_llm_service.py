import os
import unittest
from unittest.mock import patch

from services.llm_service import LLMService


class LLMServiceTests(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    @patch("services.llm_service.ChatGoogleGenerativeAI")
    def test_default_model_uses_current_gemini_flash(self, chat_model):
        LLMService()

        self.assertEqual(
            chat_model.call_args.kwargs["model"],
            "gemini-3.8-flash",
        )

    @patch.dict(
        os.environ,
        {
            "MODEL_NAME": "custom-model",
            "GOOGLE_API_KEY": "test-key",
            "TEMPERATURE": "0.5",
        },
        clear=True,
    )
    @patch("services.llm_service.ChatGoogleGenerativeAI")
    def test_model_can_still_be_overridden_by_environment(
        self, chat_model
    ):
        LLMService()

        self.assertEqual(chat_model.call_args.kwargs["model"], "custom-model")
        self.assertEqual(chat_model.call_args.kwargs["temperature"], 0.5)


if __name__ == "__main__":
    unittest.main()
