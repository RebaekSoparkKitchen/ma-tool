import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
from src.Views.RequestDialogue.RequestDialogue import RequestDialogue
from src.Models.Request import Request
from src.Connector.MA import MA


class Column(RequestDialogue):
    def __init__(self, request: Request, question: str = '请输入Column Name: ', default: str = ''):
        super().__init__(request, question, default)

    def validator(self):
        return Validator.from_callable(
            lambda x: x in ['blast_date', 'event_date', 'report_date', 'comments'],
            error_message='You can only edit blast_date, event_date, report_date, comments',
            move_cursor_to_end=True
        )

    def guess(self, text, question, default):
        return text

    def warning(self, text, question, default):
        return text



if __name__ == '__main__':
    a = 'blast_date'
    print(Column.col_name(a))