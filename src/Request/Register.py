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
import datetime as dt


def register(request: Request):
    request = wave(request)
    request = campaign_name(request)
    request = request_type(request)
    request = owner_name(request)
    request = blast_date(request)
    request = event_date(request)
    request = comments(request)
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
    request.department = ans['department']
    return request


def blast_date(request: Request, default: str = ''):
    ans = BlastDate(request=request, default=default).ask()
    if not ans:
        return comments(request=request, default=request.comments)
    request.blast_date = dt.datetime.strptime(ans, '%Y%m%d').date()
    return request


def event_date(request: Request, default: str = ''):
    if request.request_type in ['EDM', 'Newsletter']:
        return request
    ans = EventDate(request=request, default=default).ask()
    request.event_date = dt.datetime.strptime(ans, '%Y%m%d').date()
    return request


def comments(request: Request, default: str = ''):
    # ask if request.comments is None
    if not request.comments:
        request.comments = Comments(request=request, default=default).ask()
    return request


if __name__ == '__main__':
    r = Request()
    register(r)
    print(r.owner_full_name)
    print(r.campaign_name)
    print(r.blast_date)
    print(r.event_date)
    print(r.comments)
