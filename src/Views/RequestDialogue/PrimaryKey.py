from prompt_toolkit.validation import Validator

from src.Models.Request import Request
from src.Views.RequestDialogue.RequestDialogue import RequestDialogue


class PrimaryKey(RequestDialogue):
    def __init__(self, request: Request, question: str = '请输入pk_id: ', default: str = ''):
        super().__init__(request, question, default)

    def validator(self):
        return Validator.from_callable(
            lambda x: x.isdigit,
            error_message='The pk_id must be numbers',
            move_cursor_to_end=True
        )

    def guess(self, text, question, default):
        return text

    def warning(self, text, question, default):
        return text


