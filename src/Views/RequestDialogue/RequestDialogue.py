from abc import ABCMeta, abstractmethod
from src.Models.Request import Request
from src.Views.Dialogue import Dialogue


class RequestDialogue(Dialogue, metaclass=ABCMeta):
    def __init__(self, request: Request, question: str, default: str):
        super().__init__(question=question, default=default)
        self.request = request

    @abstractmethod
    def guess(self, text, question, default):
        pass

    @abstractmethod
    def warning(self, text, question, default):
        pass

    @abstractmethod
    def validator(self):
        pass
