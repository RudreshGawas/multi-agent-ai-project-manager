import os
from typing import Type

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class LLMService:
    """
    Handles all communication with the LLM.
    """

    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model=os.getenv("MODEL_NAME", "gemini-2.5-flash"),
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=float(os.getenv("TEMPERATURE", "0.2")),
        )

    def get_llm(self):
        """
        Return the base LLM.
        """
        return self.model

    def get_structured_llm(self, schema: Type):
        """
        Return an LLM configured to produce
        structured outputs matching the given schema.
        """
        return self.model.with_structured_output(schema)


llm_service = LLMService()