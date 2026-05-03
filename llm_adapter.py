"""
LLM Adapter: abstract interface + multiple provider implementations.
Swap adapters by changing LLM_PROVIDER in .env
Supported values: langchain | gemini | cohere
"""

import os
from abc import ABC, abstractmethod
from typing import List

from dotenv import load_dotenv

load_dotenv()


class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, chat_history: List[dict] = None) -> str:
        """Returns raw text response from the LLM."""


class LangChainAdapter(LLMAdapter):
    def __init__(self):
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

        self._SystemMessage = SystemMessage
        self._HumanMessage = HumanMessage
        self._AIMessage = AIMessage

        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0.8,
        )

    def generate(self, system_prompt: str, user_prompt: str, chat_history: List[dict] = None) -> str:
        messages = [self._SystemMessage(content=system_prompt)]
        for msg in (chat_history or []):
            if msg["role"] == "user":
                messages.append(self._HumanMessage(content=msg["content"]))
            else:
                messages.append(self._AIMessage(content=msg["content"]))
        messages.append(self._HumanMessage(content=user_prompt))
        return self.llm.invoke(messages).content


class GeminiAdapter(LLMAdapter):
    def __init__(self):
        from google import genai
        from google.genai import types

        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self._types = types
        self.client = genai.Client(api_key=api_key)

    def generate(self, system_prompt: str, user_prompt: str, chat_history: List[dict] = None) -> str:
        contents = []
        for msg in (chat_history or []):
            role = "user" if msg["role"] == "user" else "model"
            contents.append(self._types.Content(role=role, parts=[self._types.Part(text=msg["content"])]))
        contents.append(self._types.Content(role="user", parts=[self._types.Part(text=user_prompt)]))

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=self._types.GenerateContentConfig(system_instruction=system_prompt, temperature=0.8),
        )
        return response.text.strip()


class CohereAdapter(LLMAdapter):
    def __init__(self):
        import cohere
        api_key = os.getenv("COHERE_API_KEY", "")
        if not api_key:
            raise ValueError("COHERE_API_KEY is not set.")
        self.client = cohere.ClientV2(api_key=api_key)
        self.model = os.getenv("COHERE_MODEL", "command-r7b-12-2024")

    def generate(self, system_prompt: str, user_prompt: str, chat_history: List[dict] = None) -> str:
        messages = [{"role": "system", "content": system_prompt}]
        for msg in (chat_history or []):
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_prompt})

        response = self.client.chat(model=self.model, messages=messages)
        return response.message.content[0].text


def get_adapter() -> LLMAdapter:
    provider = os.getenv("LLM_PROVIDER", "langchain").lower()
    adapters = {
        "langchain": LangChainAdapter,
        "gemini": GeminiAdapter,
        "cohere": CohereAdapter,
    }
    if provider not in adapters:
        raise ValueError(f"Unknown LLM_PROVIDER: '{provider}'. Supported: {', '.join(adapters)}")
    return adapters[provider]()
