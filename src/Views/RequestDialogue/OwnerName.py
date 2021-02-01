import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
from rich.prompt import Confirm
from src.Views.RequestDialogue.RequestDialogue import RequestDialogue
from src.Models.Request import Request
from prompt_toolkit import prompt
from src.Views.RequestDialogue.Key_bindings import short_cut
from prompt_toolkit.completion import WordCompleter
from src.Utils.Similarity import Similarity
from rich.panel import Panel
from rich import print
from rich import box
from src.Models.Staff import Staff


class OwnerName(RequestDialogue):
    def __init__(self, request: Request = Request(), question: str = '请输入Owner Name: ', default: str = ''):
        super().__init__(request, question, default)
        self.staffs = Staff.get_all_staffs()

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
        # sort the Staff list according to the text
        staff_list = sorted(self.staffs, key=lambda x: OwnerName.compare_name((x.first_name, x.last_name), text),
                            reverse=True)
        for staff in staff_list:
            print(Panel.fit(
                '[#00FFFF]' + staff.first_name + ' ' + staff.last_name + '\n' + '[#E4007F]' + staff.team + '\n' + '['
                                                                                                                  '#E4007F]' +
                staff.location, box=box.DOUBLE_EDGE))
            command = Confirm.ask('您是指上面这个员工吗？', default=True)
            if command:
                return staff

    def ask(self):
        names = list(map(lambda x: x.first_name + ' ' + x.last_name, self.staffs))
        names = list(set(names))
        name_completer = WordCompleter(names, ignore_case=True, match_middle=True)
        ans = prompt('请输入owner的名字: ', completer=name_completer, complete_while_typing=True, key_bindings=short_cut(),
                     default=self.default, validator=self.validator())
        ans = self.warning(ans, self.question, self.default)
        ans = self.guess(ans, self.question, self.default)
        return ans

    @staticmethod
    def compare_name(standard_name: tuple, input_name: str) -> float:
        """
        helper method
        standard name: ('Ivy', 'Tan')
        input name: 'Ivy Tan'
        """
        standard_full_name = standard_name[0] + ' ' + standard_name[1]
        return Similarity.compare(standard_full_name, input_name)


if __name__ == '__main__':
    r = Request()
    o = OwnerName(r)
    staff_list = sorted(o.staffs, key=lambda x: OwnerName.compare_name((x.first_name, x.last_name), 'ivy'),
                        reverse=True)
    print(o.staffs[0])
    print(OwnerName.compare_name((o.staffs[0].first_name, o.staffs[0].last_name), 'ivy'))
    print(staff_list)
