"""
@Description: Request template
@Author: FlyingRedPig
@Date: 2020-11-24 11:07:37
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-24 11:07:38
@FilePath: \MA_tool\src\Request\Request.py
"""
import datetime as dt
from src.Control.MA import MA


class Request(MA):
    def __init__(self, request_id='', campaign_name='', request_type='', owner_first_name='',
                 owner_last_name='', owner_full_name='', department='', location='', wave='',
                 smc_campaign_id='', blast_date=None, event_date=None, creation_time=None, last_modified_time=None,
                 editor='', comments=''):
        """
        request template
        """
        super().__init__()
        self._request_id = request_id
        self._campaign_name = campaign_name
        self._request_type = request_type
        self._owner_first_name = owner_first_name
        self._owner_last_name = owner_last_name
        self._owner_full_name = owner_full_name
        self._department = department
        self._location = location
        self._wave = wave
        self._smc_campaign_id = smc_campaign_id
        self._blast_date = blast_date
        self._event_date = event_date
        self._creation_time = creation_time
        self._last_modified_time = last_modified_time
        self._editor = editor
        self._comments = comments

    def create(self):
        pass

    def edit(self):
        pass

    def delete(self):
        pass

    def check(self):
        pass

    def display(self):
        pass

    @property
    def wave(self):
        return self._wave

    @wave.setter
    def wave(self, value):
        if not value.isdigit() or int(value) <= 0:
            raise ValueError('wave should be a integer bigger than 0')
        else:
            self._wave = value

    @property
    def request_type(self):
        return self._request_type

    @request_type.setter
    def request_type(self, value):
        request_type_collection = self.readData()['standard']['request_type']
        if value not in request_type_collection:
            raise ValueError('a standard request type should be one of them : {}'.format(', '
                                                                                         ''.join(
                request_type_collection)))
        self._request_type = value

    @property
    def blast_date(self):
        return self._blast_date

    @blast_date.setter
    def blast_date(self, value: dt.date):
        if (not value) or (isinstance(value, dt.date)):
            self._blast_date = value
        else:
            raise TypeError('The blast_date type should be datetime.date or None')

    @property
    def event_date(self):
        return self._event_date

    @event_date.setter
    def event_date(self, value: dt.date):
        if (not value) or (isinstance(value, dt.date)):
            self._blast_date = value
        else:
            raise TypeError('The event_date type should be datetime.date or None')

    @property
    def owner_first_name(self):
        return self._owner_first_name

    @owner_first_name.setter
    def owner_first_name(self, value: str):
        if not value:
            raise ValueError('The owner name can not be null')
        self._owner_first_name = value

    @property
    def owner_last_name(self):
        return self._owner_last_name

    @owner_last_name.setter
    def owner_last_name(self, value: str):
        if not value:
            raise ValueError('The owner name can not be null')
        self._owner_last_name = value

    @property
    def owner_full_name(self):
        return self._owner_full_name

    @owner_full_name.setter
    def owner_full_name(self, value: str):
        if not value:
            raise ValueError('The owner name can not be null')
        self._owner_full_name = value

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value: str):
        if not value:
            raise ValueError('The department can not be null')
        self._department = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value: str):
        if not value:
            raise ValueError('There should be an owner name for a certain campaign')
        self._location = value

    @property
    def campaign_name(self):
        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, value: str):
        if not value:
            raise ValueError('There should be a campaign name for a certain campaign')
        self._campaign_name = value

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value: str):
        if not self.blast_date and not value:
            raise ValueError('You must write some comments when there is no blast date')
        self._comments = value

    @property
    def smc_campaign_id(self):
        return self._smc_campaign_id

    @smc_campaign_id.setter
    def smc_campaign_id(self, value: str):
        self._smc_campaign_id = value

    @property
    def editor(self):
        return self._editor

    @editor.setter
    def editor(self, value: str):
        self._editor = value

    @property
    def request_id(self):
        return self._request_id

    @request_id.setter
    def request_id(self, value: str):
        self._request_id = value

    @property
    def creation_time(self):
        return self._creation_time

    @creation_time.setter
    def creation_time(self, value: dt.datetime):
        if (not value) or (isinstance(value, dt.datetime)):
            self._blast_date = value
        else:
            raise TypeError('The creation_time type should be datetime.datetime or None')

    @property
    def last_modified_time(self):
        return self._last_modified_time

    @last_modified_time.setter
    def last_modified_time(self, value: dt.datetime):
        if (not value) or (isinstance(value, dt.datetime)):
            self._blast_date = value
        else:
            raise TypeError('The last_modified_time type should be datetime.datetime or None')

