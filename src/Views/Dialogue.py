from abc import ABCMeta, abstractmethod
from typing import Union
from prompt_toolkit import prompt
from src.Connector.MA import MA


class Dialogue(MA, metaclass=ABCMeta):
    def __init__(self, question: str, default: str):
        """
        The standard way to raise a dialogue, we have question / default as parameters for changing, request as a
        context, we need to do some validation / warnings according to the context
        :param question: user's question
        :param default: default input
        """
        super().__init__()
        self.question = question
        self.default = default

    def ask(self) -> Union[str, dict]:
        ans = prompt(self.question, default=self.default, validator=self.validator())
        ans = self.warning(ans, self.question, self.default)
        ans = self.guess(ans, self.question, self.default)
        return ans

    @abstractmethod
    def guess(self, text, question, default):
        pass

    @abstractmethod
    def warning(self, text, question, default):
        pass

    @abstractmethod
    def validator(self):
        pass
