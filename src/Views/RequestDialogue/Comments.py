import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
from src.Views.RequestDialogue.Dialogue import Dialogue
from src.Models.Request import Request


class Comments(Dialogue):
    def __init__(self, request: Request, question: str = '请输入 comments: ', default: str = ''):
        super().__init__(request, question, default)

    def validator(self):
        return Validator.from_callable(
            # comments and blast date can not be null at the same time
            lambda x: x or self.request.blast_date,
            error_message='pls comment why you have no blast date',
            move_cursor_to_end=True
        )

    def guess(self, text, question, default):
        return text

    def warning(self, text, question, default):
        return text
