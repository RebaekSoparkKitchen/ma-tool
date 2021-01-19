import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
from src.Views.RequestDialogue.RequestDialogue import RequestDialogue
from src.Models.Request import Request
from src.Connector.MA import MA
from src.Views.RequestDialogue.BlastDate import BlastDate
from src.Views.RequestDialogue.EventDate import EventDate
from src.Utils.DateHelper import DateHelper

class ReportDate(RequestDialogue):
    """
    通常情况下，report date会被自动计算，但是在request update里面是给自定义的接口的，所以此类会在update时被调用，而非create时。
    """
    def __init__(self, request: Request, question: str = '请输入Report Date: ', default: str = '', column=''):
        super().__init__(request, question, default)
        self.column = column

    def validator(self):
        return Validator.from_callable(
            lambda x: DateHelper.is_date(x) and self.verify(x),
            error_message='The value can not be blank and report date should be later than blast date',
            move_cursor_to_end=True
        )

    def verify(self, text):
        """
        当定义 report_date 时，其必须不能早于 blast_date
        :param text:
        :return:
        """
        report_date = DateHelper.str_to_date(text)
        if report_date < self.request.blast_date:
            return False
        return True

    def guess(self, text, question, default):
        return text

    def warning(self, text, question, default):
        return text




if __name__ == '__main__':
    pass
