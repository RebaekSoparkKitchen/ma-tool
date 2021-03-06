import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
import datetime as dt
from rich.prompt import Confirm
from src.Views.RequestDialogue.RequestDialogue import RequestDialogue
from src.Models.Request import Request
from src.Utils.DateHelper import DateHelper


class EventDate(RequestDialogue):
    def __init__(self, request: Request, question: str = '请输入Event Date: ', default: str = ''):
        super().__init__(request, question, default)
        if default == '':
            self.default = self.read_data()['default']['event_date']
        elif isinstance(default, dt.date):
            self.default = str(default)

    def verify_event_date(self, text: str):
        """
        helper method
        :param text: the user's input, should be a str like yyyymmdd, and can not be None when request type == webinar
        :return: true if the input can be translated to a dt.date successfully
        """
        if text == '':
            return self.request.request_type not in ['Webinar Invitation', 'Offline Event Invitation']
        elif self.request.request_type in ['EDM', 'Newsletter', 'Nurture']:
            return False
        return True

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
        implements method, validator for event date
        :return: Validator
        """
        return Validator.from_callable(
            lambda x: DateHelper.is_date(x) and self.verify_event_date(x),
            error_message='The format should be yyyymmdd / yyyy-mm-dd, eg: 20200305, 2020-03-05',
            move_cursor_to_end=True
        )

    def warning(self, text, question, default):
        """
        implements method, warnings for event date
        :param text: user's input
        :param question: the prompt's question
        :param default: the prompt's default
        :return:
        """

        event_date = DateHelper.str_to_date(text)
        if self.request.blast_date:
            blast_date = self.request.blast_date
            while not EventDate.confirm_date(event_date, blast_date,
                                             '[#ffc107]您输入的event date日期({})在blast date({})之前，您确定吗？'.format(event_date,
                                                                                                           self.request.blast_date)):
                return self.ask()

        while not EventDate.confirm_date(event_date, dt.date.today(),
                                         '[#ffc107]您输入的event date日期({})在今天之前，您确定吗？'.format(event_date)):
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
    r.blast_date = dt.date(2020, 12, 14)
    e = EventDate(r)
    ans = e.ask()
    print(ans)
