import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
from rich.prompt import Confirm
from src.Views.RequestDialogue.Dialogue import Dialogue
from src.Models.Request import Request
from prompt_toolkit import prompt
from src.Views.RequestDialogue.Key_bindings import short_cut
from prompt_toolkit.completion import WordCompleter
from src.Utils.Similarity import Similarity
from rich.panel import Panel
from rich import print
from rich import box


class OwnerName(Dialogue):
    def __init__(self, request: Request = Request(), question: str = '请输入Owner Name: ', default: str = ''):
        super().__init__(request, question, default)
        self.name_list = self.sql_process("SELECT first_name, last_name FROM Staff")

        if default == '':
            self.default = self.read_data()['default']['owner_full_name']

    def validator(self):
        return Validator.from_callable(
            lambda x: True,
            error_message='The name should be string',
            move_cursor_to_end=True
        )

    def warning(self, text, question, default):
        return text

    def guess(self, text, question, default):
        for item in self.search_name(text):
            guess_name = item[0]
            team = self.info(guess_name)[0][0]
            location = self.info(guess_name)[0][1]
            print(Panel.fit(
                '[#00FFFF]' + guess_name[0] + ' ' + guess_name[1] + '\n' + '[#E4007F]' + team + '\n' + '[#E4007F]' +
                location, box=box.DOUBLE_EDGE))

            command = Confirm.ask('您是指上面这个员工吗？', default=True)

            if command:
                return {'owner_first_name': guess_name[0], 'owner_last_name': guess_name[1], 'owner_full_name':
                    ' '.join(guess_name), 'team': team, 'location': location}

    def ask(self):
        name_completer = WordCompleter(list(map(lambda x: ' '.join(x), self.name_list)), ignore_case=True,
                                       match_middle=True)
        ans = prompt('请输入owner的名字: ', completer=name_completer, complete_while_typing=True, key_bindings=short_cut(),
                     default=self.default)
        ans = self.warning(ans, self.question, self.default)
        ans = self.guess(ans, self.question, self.default)
        return ans

    def search_name(self, input_name: str) -> list:
        """
        name: the input name
        """
        new_name = []
        for name in self.name_list:
            new_name.append([name, OwnerName.compare_name(name, input_name)])

        new_name.sort(key=lambda x: x[1], reverse=True)
        return new_name

    @staticmethod
    def compare_name(standard_name: tuple, input_name: str) -> float:
        """
        helper method
        standard name: ('Ivy', 'Tan')
        input name: 'Ivy Tan'
        """
        standard_full_name = standard_name[0] + ' ' + standard_name[1]
        return Similarity.compare(standard_full_name, input_name)

    def info(self, name: tuple):
        """
        return : team , location when input name
        """
        return self.sql_process(
            f"SELECT team, location FROM Staff WHERE first_name = '{name[0]}' AND last_name = '{name[1]}'")


if __name__ == '__main__':
    r = Request()
    o = OwnerName(r)
    print(o.ask())
