"""
@Description: Request template
@Author: FlyingRedPig
@Date: 2020-11-24 11:07:37
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-24 11:07:38
@FilePath: \MA_tool\src\Request\Request.py
"""
import datetime as dt
from rich import print, box
from rich.panel import Panel
from src.Connector.MA import MA
import src.Utils.AttributeToStr as attr



class Request:
    def __init__(self, request_id='', wave='', smc_campaign_id='', campaign_name='', request_type='',
                 owner_full_name='', owner_first_name='',
                 owner_last_name='', team='', mu='', location='',
                 blast_date='', event_date='', report_date='', creation_time='',
                 last_modified_time='',
                 editor='', comments='', request_status=0):
        """
        request template
        """
        super().__init__()
        self._request_id = request_id
        self._wave = wave
        self._smc_campaign_id = smc_campaign_id
        self._campaign_name = campaign_name
        self._request_type = request_type
        self._owner_full_name = owner_full_name
        self._owner_first_name = owner_first_name
        self._owner_last_name = owner_last_name
        self._team = team
        self._mu = mu  # 依据location做一个mapping
        self._location = location
        try:
            self._blast_date = dt.datetime.strptime(blast_date, '%Y-%m-%d').date()
        except ValueError:
            try:
                self._blast_date = dt.datetime.strptime(blast_date, '%Y%m%d').date()
            except ValueError:
                self._blast_date = blast_date

        try:
            self._event_date = dt.datetime.strptime(event_date, '%Y-%m-%d').date()
        except ValueError:
            try:
                self._event_date = dt.datetime.strptime(event_date, '%Y%m%d').date()
            except ValueError:
                self._event_date = event_date

        self._report_date = report_date
        self._creation_time = creation_time
        self._last_modified_time = last_modified_time
        self._editor = editor
        self._comments = comments
        self._request_status = request_status

    def create(self):
        ma = MA()
        db_data = ma.read_data('Database')
        request_db = db_data['Request']
        col, values = attr.transfer(self)
        col = tuple(map(lambda x: request_db[x], col))
        values = tuple(map(lambda x: str(x), values))
        sql = f"INSERT INTO Request {str(col)} VALUES {str(values)}"
        ma.sql_process(sql)
        return

    def edit(self):
        pass

    @staticmethod
    def delete(index: int):

        sql = f"UPDATE Request SET request_status = -2 WHERE id={index}"
        ma = MA()
        ma.sql_process(sql)
        return

    @staticmethod
    def check(index: int):
        """
        :param index: primary key for request
        :return:
        """

        sql = f"SELECT * FROM Request WHERE request_status != -2 and id = {index}"
        result = MA().sql_process(sql)

        if len(result) > 1:
            raise ValueError("请赶快检查：同一个request id不可以有两个wave")

        if not result:
            return None

        values = MA().sql_process(sql)[0][1:]  # index 0 is primary key id
        request = Request(*values)

        return request

    def display(self):
        request_vars = vars(self)
        info = ''

        for item in request_vars:
            if item in ['_owner_first_name', '_owner_last_name', '_mu', '_creation_time', '_last_modified_time',
                        '_editor', '_report_date']:
                continue
            if request_vars[item]:
                info += f'[#E4007F]{self.str_process(item[1:])}:[/#E4007F] [#00FFFF]{request_vars[item]}[/#00FFFF] \n'
        # [:-2]去除最后的一个\n折行
        print(Panel.fit(info[:-2], box=box.DOUBLE))

    @staticmethod
    def str_process(col_name: str) -> str:
        """
        transfer the lower case staff to the first capital words
        :param col_name: eg. campaign_name
        :return: eg. Campaign Name
        """
        if col_name == 'id':
            return col_name.upper()
        return col_name.replace('_', ' ').title()

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
        ma = MA()
        request_type_collection = ma.read_data()['standard']['request_type']
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
            self._event_date = value
        else:
            raise TypeError('The event_date type should be datetime.date or None')

    @property
    def report_date(self):
        return self._report_date

    @report_date.setter
    def report_date(self, value: dt.date):
        if (not value) or (isinstance(value, dt.date)):
            self._report_date = value
        else:
            raise TypeError('The report_date type should be datetime.date or None')

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
    def team(self):
        return self._team

    @team.setter
    def team(self, value: str):
        if not value:
            raise ValueError('The team can not be null')
        self._team = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value: str):
        if not value:
            raise ValueError('There should be an owner name for a certain campaign')
        self._location = value

    @property
    def mu(self):
        return self._mu

    @mu.setter
    def mu(self, value: str):
        ma = MA()
        mu_collection = ma.read_data()['standard']['mu']
        if value not in mu_collection:
            raise ValueError('a standard mu should be one of them : {}'.format(', '.join(mu_collection)))
        self._mu = value

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
            self._creation_time = value
        else:
            raise TypeError('The creation_time type should be datetime.datetime or None')

    @property
    def last_modified_time(self):
        return self._last_modified_time

    @last_modified_time.setter
    def last_modified_time(self, value: dt.datetime):
        if (not value) or (isinstance(value, dt.datetime)):
            self._last_modified_time = value
        else:
            raise TypeError('The last_modified_time type should be datetime.datetime or None')

    @property
    def request_status(self):
        return self._request_status

    @request_status.setter
    def request_status(self, value: int):
        self._request_status = value


if __name__ == '__main__':
    r = Request()
    print(r.display())
