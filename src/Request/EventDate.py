import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
import datetime as dt
from rich.prompt import Confirm
from src.Request.Dialogue import Dialogue
from src.Request.Request import Request


class EventDate(Dialogue):
    def __init__(self, request: Request, question: str = '请输入Event Date: ', default: str = ''):
        super().__init__(request, question, default)
        if default == '':
            self.default = self.readData()['default']['event_date']

    def verify_event_date(self, text: str):
        """
        helper method
        :param text: the user's input, should be a str like yyyymmdd, and can not be None when request type == webinar
        :return: true if the input can be translated to a dt.date successfully
        """
        if text == '':
            return self.request.request_type not in ['Webinar Invitation', 'Offline Invitation']
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
        implements method, validator for event date
        :return: Validator
        """
        return Validator.from_callable(
            self.verify_event_date,
            error_message='The format should be yyyymmdd, eg: 20200305',
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

        event_date = dt.datetime.strptime(text, '%Y%m%d').date()
        if self.request.blast_date:
            while not EventDate.confirm_date(event_date, self.request.blast_date,
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
