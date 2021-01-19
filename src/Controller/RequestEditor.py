import sys

sys.path.append("../..")
import src.Utils.SqlHelper as sql_helper
from src.Connector.MA import MA
from src.Models.Request import Request
from src.Utils.DateHelper import DateHelper
from src.Utils.ReportDate import report_date_gen
from src.Views.RequestDialogue.Column import Column
from src.Views.RequestDialogue.PrimaryKey import PrimaryKey
from src.Views.RequestDialogue.Value import Value


class RequestEditor(object):
    def __init__(self):
        self.table = 'Request'
        self.pk_id = ''
        self.col = ''
        self.value = ''

    def dialogue(self):
        """
        整体描述Request在update过程中的对话过程
        :return:
        """
        request = Request()
        pk_id = PrimaryKey(request).ask()
        request = Request.check(int(pk_id))
        column = Column(request).ask()
        value = str(Value(request).ask())
        self.pk_id = pk_id
        self.col = column
        self.value = value
        self.date_process(request)

    def date_process(self, request: Request):
        if self.col == 'blast_date':
            blast = DateHelper.str_to_date(self.value)
            event = request.event_date
            new_report_date = report_date_gen(blast, event)
            self.col = [self.col, 'report_date']
            self.value = [blast, new_report_date]
        elif self.col == 'event_date':
            blast = request.blast_date
            event = DateHelper.str_to_date(self.value)
            new_report_date = report_date_gen(blast, event)
            self.col = [self.col, 'report_date']
            self.value = [event, new_report_date]
        elif self.col == 'report_date':
            self.value = DateHelper.str_to_date(self.value)

    def update(self):
        self.dialogue()
        statement = sql_helper.update(self.table, self.col, self.value, int(self.pk_id))
        MA().query(statement)

if __name__ == '__main__':
    r = RequestEditor()
    r.update()
