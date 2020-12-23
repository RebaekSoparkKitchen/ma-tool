import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
import datetime as dt
from rich.prompt import Confirm
from src.Views.RequestDialogue.RequestDialogue import RequestDialogue
from src.Models.Request import Request


class BlastDate(RequestDialogue):
    def __init__(self, request: Request = Request(), question: str = '请输入Blast Date: ', default: str = ''):
        super().__init__(request, question, default)
        if default == '':
            self.default = self.read_data()['default']['blast_date']
        elif isinstance(default, dt.date):
            self.default = default.strftime('%Y%m%d')

    @staticmethod
    def is_date(text: str):
        """
        helper method
        :param text: the user's input, should be a str like yyyymmdd
        :return: true if the input can be translated to a dt.date successfully
        """
        if text == '':
            return True
        try:
            dt.datetime.strptime(text, '%Y%m%d').date()
            return True
        except ValueError:
            return False

    @staticmethod
    def confirm_date(date1: dt.date, date2: dt.date, question: str):
        """
        helper method
        :param date1: date to be compared
        :param date2: date to be compared
        :param question: once date compared surprise, we should ask customer to confirm
        :return: True or trigger a confirm dialogue
        """
        if date1 < date2:
            confirm = Confirm.ask(question)
            return confirm
        return True

    def validator(self):
        """
        implements method, validator for blast date
        :return: Validator
        """
        return Validator.from_callable(
            BlastDate.is_date,
            error_message='The format should be yyyymmdd, eg: 20200305',
            move_cursor_to_end=True
        )

    def warning(self, text, question, default):
        """
        implements method, warnings for blast date
        :param text: user's input
        :param question: the prompt's question
        :param default: the prompt's default
        :return:
        """
        # the process for the null value
        if text == '':
            command = Confirm.ask('您确认此需求没有blast date吗', default=True)
            if command:
                return text
            else:
                # below line means: stop this function, shut down everything, I want to run self.ask() again
                return self.ask()

        blast_date = dt.datetime.strptime(text, '%Y%m%d').date()
        while not BlastDate.confirm_date(blast_date, dt.date.today(),
                                         f'[#ffc107]您输入的blast date日期{blast_date}在今天之前，您确定吗？'):
            return self.ask()

        if self.request.event_date:
            event_date = self.request.event_date

            while not self.confirm_date(event_date, blast_date,
                                        f'[#ffc107]您输入的blast date日期({blast_date})在event date({event_date})之后，您确定吗？'):
                return self.ask()

        return text

    def guess(self, text, question, default):
        """
        no guess for this class, just implements
        :param text:
        :param question:
        :param default:
        :return:
        """
        return text


if __name__ == '__main__':
    r = Request()
    r.request_type = 'Webinar Invitation'
    b = BlastDate(r)
    ans = b.ask()
    print(ans)
