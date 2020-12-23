import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
from src.Views.RequestDialogue.Dialogue import Dialogue
from src.Models.Request import Request


class Wave(Dialogue):
    def __init__(self, request: Request, question: str = '请输入 wave: ', default: str = ''):
        super().__init__(request, question, default)
        if default == '':
            self.default = self.read_data()['default']['wave']

    def validator(self):
        return Validator.from_callable(
            lambda x: x.isdigit() and int(x) > 0,
            error_message='Wave should be integers bigger than 0',
            move_cursor_to_end=True
        )

    def guess(self, text, question, default):
        return text

    def warning(self, text, question, default):
        return text


if __name__ == '__main__':
    r = Request()
    w = Wave(r)
    print(w.ask())
