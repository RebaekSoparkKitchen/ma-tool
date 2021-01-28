import sys

sys.path.append("../..")
from src.Views.RequestDialogue.CampaignName import CampaignName
from src.Views.RequestDialogue.RequestType import RequestType
from src.Views.RequestDialogue.OwnerName import OwnerName
from src.Views.RequestDialogue.EventDate import EventDate
from src.Views.RequestDialogue.BlastDate import BlastDate
from src.Views.RequestDialogue.Comments import Comments
from src.Models.Request import Request
from src.Views.RequestDialogue.Wave import Wave
from src.Views.RequestDialogue.MoreWave import MoreWave
from src.Utils.ReportDate import report_date_gen
import datetime as dt
from rich.prompt import Confirm
from src.Connector.MA import MA
from src.Utils.DateHelper import DateHelper


def register(request: Request):
    request = wave(request=request, default=request.wave)
    if int(request.wave) == 1:
        request = wave_one_process(request)
    else:
        index = MoreWave(request).ask()
        request = wave_else_process(request, int(index))

    request.display()
    if not Confirm.ask('请最终确定一下此request的信息', default=True):
        return register(request)

    return request


def wave_one_process(request: Request):
    request = campaign_name(request, default=request.campaign_name)
    request = request_type(request, default=request.request_type)
    request = owner_name(request, default=request.owner_full_name)
    request = blast_date(request, default=request.blast_date)
    request = event_date(request, default=request.event_date)
    request = comments(request, default=request.comments)
    request = request_id(request=request)

    request = report_date(request=request)
    request = editor(request=request)
    request = creation_time(request=request)
    request = last_modified_time(request=request)
    return request


def wave_else_process(request: Request, index: int):
    new_wave = request.wave
    request = Request.check(index)
    request.wave = new_wave
    request = blast_date(request)
    request.comments = ''
    request = comments(request, default='')
    request.smc_campaign_id = ''
    request.request_status = 0

    request = report_date(request=request)
    request = editor(request=request)
    request = creation_time(request=request)
    request = last_modified_time(request=request)
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
    request.owner_first_name = ans.first_name
    request.owner_last_name = ans.last_name
    request.owner_full_name = ans.first_name + ' ' + ans.last_name
    request.location = ans.location
    request.mu = ans.location.split(',')[1][1:]
    request.team = ans.team
    return request


def blast_date(request: Request, default: str = ''):
    ans = BlastDate(request=request, default=default).ask()
    if not ans:
        return comments(request=request, default=request.comments)
    request.blast_date = DateHelper.str_to_date(ans)
    return request


def event_date(request: Request, default: str = ''):
    if request.request_type in ['EDM', 'Newsletter']:
        request.event_date = ''
        return request
    ans = EventDate(request=request, default=default).ask()
    request.event_date = DateHelper.str_to_date(ans)
    return request


def report_date(request: Request):
    request.report_date = report_date_gen(request.blast_date, request.event_date)
    return request


def comments(request: Request, default: str = ''):
    request.comments = Comments(request=request, default=default).ask()
    return request


def request_id(request: Request):
    ma = MA()
    max_id = ma.query("SELECT MAX(request_id) FROM Request")
    request.request_id = max_id[0][0] + 1

    return request


def editor(request: Request):
    ma = MA()
    request.editor = ma.read_config()["username"]
    return request


def creation_time(request: Request):
    request.creation_time = dt.datetime.now()
    return request


def last_modified_time(request: Request):
    request.last_modified_time = dt.datetime.now()
    return request


if __name__ == '__main__':
    # campaign name要自动变更
    r = Request()
    r = register(r)
    r.display()
    # result = model.Request.select().where(model.Request.request_id == '966').get()
    # query = model.Request.select().where(model.Request.request_id == '966')
    # for item in query:
    #     print(item.campaign_name)
