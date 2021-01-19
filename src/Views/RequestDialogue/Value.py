import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
from src.Views.RequestDialogue.RequestDialogue import RequestDialogue
from src.Models.Request import Request
from src.Connector.MA import MA
from src.Views.RequestDialogue.BlastDate import BlastDate
from src.Views.RequestDialogue.EventDate import EventDate

class Value(RequestDialogue):
    """
    Value比较特殊，它需要额外接收参数 Column，并以此为依据制作validator
    """
    def __init__(self, request: Request, question: str = '请输入Value: ', default: str = '', column=''):
        super().__init__(request, question, default)
        self.column = column

    def validator(self):
        if self.column == 'blast_date':
            return BlastDate().validator()
        else:
            return Validator.from_callable(
                lambda x: x,
                error_message='The value can not be blank',
                move_cursor_to_end=True
            )

    def guess(self, text, question, default):
        return text

    def warning(self, text, question, default):
        return text




if __name__ == '__main__':
    pass
