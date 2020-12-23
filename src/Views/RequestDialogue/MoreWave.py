import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
from src.Views.RequestDialogue.RequestDialogue import RequestDialogue
from src.Models.Request import Request


class MoreWave(RequestDialogue):
    def __init__(self, request: Request, question: str = '请输入wave1 index: ', default: str = ''):
        super().__init__(request, question, default)

    def validator(self):
        return Validator.from_callable(
            lambda x: x.isdigit,
            error_message='The index must be a number',
            move_cursor_to_end=True
        )

    def guess(self, text, question, default):
        return text

    def warning(self, text, question, default):
        return text



