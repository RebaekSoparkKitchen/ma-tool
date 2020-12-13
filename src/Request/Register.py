import sys

sys.path.append("../..")
from src.Request.CampaignName import CampaignName
from src.Request.RequestType import RequestType
from src.Request.OwnerName import OwnerName
from src.Request.EventDate import EventDate
from src.Request.BlastDate import BlastDate
from src.Request.Comments import Comments
from src.Request.Request import Request
from src.Request.Wave import Wave
from src.Utils.ReportDate import report_date_gen
import datetime as dt
from rich.prompt import Confirm
from src.Control.MA import MA
from src.Utils.Database import get_col_name


def register(request: Request):
    request = wave(request=request, default=request.wave)
    if int(request.wave) == 1:
        request = wave_one_process(request)
    else:
        request = wave_else_process()
    return request


def wave_one_process(request: Request):
    request = campaign_name(request, default=request.campaign_name)
    request = request_type(request, default=request.request_type)
    request = owner_name(request, default=request.owner_full_name)
    request = blast_date(request, default=request.blast_date)
    request = event_date(request, default=request.event_date)
    request = comments(request, default=request.comments)
    request = request_id(request=request)
    request.display()

    if not Confirm.ask('请最终确定一下此request的信息', default=True):
        return register(request)

    request = report_date(request=request)
    request = editor(request=request)
    request = creation_time(request=request)
    request = last_modified_time(request=request)
    return request


def wave_else_process():
    request = Request.check()
    request = blast_date(request)
    request.comments = ''
    request = comments(request, default='')
    return request


def wave(request: Request, default: str = '') -> Request:
    request.wave = Wave(request=request, default=default).ask()
    return request


def campaign_name(request: Request, default: str = ''):
    request.campaign_name = CampaignName(request=request, default=default).ask()
    return request


def request_type(request: Request, default: str = ''):
    request.request_type = RequestType(request=request, default=default).ask()
    return request


def owner_name(request: Request, default: str = ''):
    ans = OwnerName(request=request, default=default).ask()
    request.owner_first_name = ans['owner_first_name']
    request.owner_last_name = ans['owner_last_name']
    request.owner_full_name = ans['owner_full_name']
    request.location = ans['location']
    request.mu = ans['location'].split(',')[1][1:]
    request.team = ans['team']
    return request


def blast_date(request: Request, default: str = ''):
    ans = BlastDate(request=request, default=default).ask()
    if not ans:
        return comments(request=request, default=request.comments)
    request.blast_date = dt.datetime.strptime(ans, '%Y%m%d').date()
    return request


def event_date(request: Request, default: str = ''):
    if request.request_type in ['EDM', 'Newsletter']:
        request.event_date = ''
        return request
    ans = EventDate(request=request, default=default).ask()
    request.event_date = dt.datetime.strptime(ans, '%Y%m%d').date()
    return request


def report_date(request: Request):
    request.report_date = report_date_gen(request.blast_date, request.event_date)
    return request


def comments(request: Request, default: str = ''):
    # ask if request.comments is None
    if not request.comments:
        request.comments = Comments(request=request, default=default).ask()
    return request


def request_id(request: Request):
    ma = MA()
    max_id = ma.sqlProcess("SELECT MAX(request_id) FROM Request")
    request.request_id = max_id[0][0] + 1

    return request


def editor(request: Request):
    ma = MA()
    request.editor = ma.readConfig()["username"]
    return request


def creation_time(request: Request):
    request.creation_time = dt.datetime.now()
    return request


def last_modified_time(request: Request):
    request.last_modified_time = dt.datetime.now()
    return request


if __name__ == '__main__':
    # campaign name要自动变更
    # r = Request()
    # r = register(r)
    # r.create()
    print(Request.check('966-1'))
    print(get_col_name('Request'))
