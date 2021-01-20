import sys

sys.path.append("../..")
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from src.Views.RequestDialogue.Key_bindings import short_cut

from prompt_toolkit.validation import Validator
from src.Views.RequestDialogue.RequestDialogue import RequestDialogue
from src.Models.Request import Request


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

    def ask(self):
        col_list = ['blast_date', 'event_date', 'report_date', 'comments']
        name_completer = WordCompleter(col_list, ignore_case=True, match_middle=True)
        ans = prompt('请输入Column Name: ', completer=name_completer, complete_while_typing=True, key_bindings=short_cut(),
                     default=self.default, validator=self.validator())
        ans = self.warning(ans, self.question, self.default)
        ans = self.guess(ans, self.question, self.default)
        return ans


if __name__ == '__main__':
    a = 'blast_date'
    print(Column.col_name(a))
