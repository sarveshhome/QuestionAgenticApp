from abc import ABC, abstractmethod
from typing import List
from llm_adapter import get_adapter


class BaseAgent(ABC):
    def __init__(self):
        self.adapter = get_adapter()

    @abstractmethod
    def run(self, **kwargs) -> dict:
        """Execute the agent's task and return result."""

    def call_llm(self, system_prompt: str, user_prompt: str, chat_history: List[dict] = None) -> str:
        return self.adapter.generate(system_prompt, user_prompt, chat_history)
