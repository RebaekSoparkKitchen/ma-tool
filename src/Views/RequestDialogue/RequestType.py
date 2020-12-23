import sys

sys.path.append("../..")
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from src.Views.RequestDialogue.Key_bindings import short_cut

from prompt_toolkit.validation import Validator
from src.Views.RequestDialogue.RequestDialogue import RequestDialogue
from src.Models.Request import Request


class RequestType(RequestDialogue):
    def __init__(self, request: Request, question: str = '请输入 request type: ', default: str = ''):
        super().__init__(request, question, default)
        self.request_type_collection = self.read_data()['standard']['request_type']
        if default == '':
            self.default = self.read_data()['default']['request_type']

    def validator(self):
        return Validator.from_callable(
            lambda x: x in self.request_type_collection,
            error_message='a standard request type should be one of them : {}'.format(', '
                                                                                      ''.join(self.request_type_collection)),
            move_cursor_to_end=True
        )

    def guess(self, text, question, default):
        return text

    def warning(self, text, question, default):
        return text

    def ask(self) -> str:
        request_type_completer = WordCompleter(self.request_type_collection, ignore_case=True, match_middle=True)
        ans = prompt('请输入 Request Type: ', default=self.default, completer=request_type_completer,
                     complete_while_typing=True,
                     key_bindings=short_cut(),
                     validator=self.validator())
        ans = self.warning(ans, self.question, self.default)
        ans = self.guess(ans, self.question, self.default)
        return ans


if __name__ == '__main__':
    r = Request()
    t = RequestType(r)
    print(t.ask())
