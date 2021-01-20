import sys

sys.path.append("../..")
import src.Utils.SqlHelper as sql_helper
from src.Connector.MA import MA
from src.Models.Request import Request
from src.Utils.DateHelper import DateHelper
from src.Utils.ReportDate import report_date_gen
from src.Views.Diagram.Panel import Panel
from src.Views.RequestDialogue.Column import Column
from src.Views.RequestDialogue.PrimaryKey import PrimaryKey
from src.Views.RequestDialogue.ReportDate import ReportDate
from src.Views.RequestDialogue.BlastDate import BlastDate
from src.Views.RequestDialogue.EventDate import EventDate
from src.Views.RequestDialogue.Comments import Comments
from src.Models.TableData import data_producer


class RequestEditor(object):
    def __init__(self):
        self.table = 'Request'
        self.pk_id = ''
        self.col = ''
        self.value = ''


    def read(self) -> None:
        request = Request()
        pk_id = PrimaryKey(request).ask()
        self.pk_id = pk_id
        self.display(self.pk_id)

    def dialogue(self) -> None:
        """
        整体描述Request在update过程中的对话过程
        :return:
        """
        self.read()
        request = Request.check(int(self.pk_id))
        column = Column(request).ask()
        self.col = column
        if column == 'blast_date':
            self.blast_date_process(request)
        elif column == 'event_date':
            self.event_date_process(request)
        elif column == 'report_date':
            self.report_date_process(request)
        elif column == 'comments':
            self.comments_process(request)

    def blast_date_process(self, request: Request) -> None:
        """
        blast_date和下面的event_date这么长是因为要重新计算event_date
        :param request:
        :return:
        """
        self.value = BlastDate(request, default=request.blast_date).ask()
        blast = DateHelper.str_to_date(self.value)
        event = request.event_date
        new_report_date = report_date_gen(blast, event)
        self.col = ['blast_date', 'report_date']
        self.value = [blast, new_report_date]

    def event_date_process(self, request: Request) -> None:
        self.value = EventDate(request, default=request.event_date).ask()
        blast = request.blast_date
        event = DateHelper.str_to_date(self.value)
        new_report_date = report_date_gen(blast, event)
        self.col = ['event_date', 'report_date']
        self.value = [event, new_report_date]

    def report_date_process(self, request: Request) -> None:
        self.value = ReportDate(request, default=request.report_date).ask()

    def comments_process(self, request: Request) -> None:
        self.value = Comments(request, default=request.comments).ask()


    def display(self, pk_id: int):
        cols = ['id', 'wave', 'campaign_name', 'owner_full_name', 'team', 'mu', 'blast_date', 'event_date',
                'report_date', 'comments']
        sql = f"SELECT {','.join(cols)} FROM Request WHERE id = {pk_id}"
        result = MA().query(sql, as_dict=True)[0]
        data = data_producer('', list(result.keys()), sql)
        print(data.cols)
        print(data.content)
        panel = Panel(data).display()
        panel.__next__()

    def update(self):
        """
        主方法
        :return:
        """
        self.dialogue()
        statement = sql_helper.update(self.table, self.col, self.value, int(self.pk_id))
        MA().query(statement)

if __name__ == '__main__':
    r = RequestEditor()
    r.update()
