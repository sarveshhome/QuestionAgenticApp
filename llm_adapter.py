"""
LLM Adapter: abstract interface + LangChain implementation.
Swap adapters by changing LLM_PROVIDER in .env (default: langchain).
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


def get_adapter() -> LLMAdapter:
    provider = os.getenv("LLM_PROVIDER", "langchain").lower()
    if provider == "langchain":
        return LangChainAdapter()
    raise ValueError(f"Unknown LLM_PROVIDER: '{provider}'. Supported: langchain")
