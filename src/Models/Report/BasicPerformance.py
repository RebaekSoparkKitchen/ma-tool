import datetime as dt
from src.Connector.MA import MA
from src.Utils.SqlHelper import insert
from src.Models.Report.ClickPerformance import ClickPerformance

class BasicPerformance(object):

    def __init__(self, data):
        self.smc_campaign_id = data['smc_campaign_id']
        self.sent = int(data['sent'])
        self.hard_bounces = int(data['hard_bounces'])
        self.soft_bounces = int(data['soft_bounces'])
        self.delivered = int(data['delivered'])
        self.opened = int(data['opened'])
        self.click = int(data['click'])
        self.unique_click = int(data['unique_click'])
        self.valid_click = ClickPerformance.valid_click_number(self.smc_campaign_id)

        try:
            self.bounce_rate = (self.hard_bounces + self.soft_bounces) / self.sent
        except ZeroDivisionError:
            self.bounce_rate = 0

        try:
            self.open_rate = self.opened / self.delivered
        except ZeroDivisionError:
            self.bounce_rate = 0

        try:
            self.unique_click_to_open_rate = self.unique_click / self.opened
        except ZeroDivisionError:
            self.unique_click_to_open_rate = 0

        try:
            self.valid_click_to_open_rate = self.valid_click / self.opened
        except ZeroDivisionError:
            self.vanilla_click_to_open_rate = 0

        try:
            self.vanilla_click_to_open_rate = self.click / self.opened
        except ZeroDivisionError:
            self.vanilla_click_to_open_rate = 0

        try:
            self.ctr = self.click / self.delivered
        except ZeroDivisionError:
            self.ctr = 0

        try:
            self.unique_ctr = self.unique_click / self.delivered
        except ZeroDivisionError:
            self.unique_ctr = 0


    @staticmethod
    def select(smc_campaign_id: int or str):
        sql = f"SELECT * FROM BasicPerformance WHERE smc_campaign_id = {smc_campaign_id}"
        rows = MA().query(sql, as_dict=True)[0]
        return BasicPerformance(rows)

    def update(self):
        table = "BasicPerformance"
        data_dic = self.__dict__
        data_dic['editor'] = MA().read_config()['username']
        data_dic['creation_time'] = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql1 = f"DELETE FROM BasicPerformance WHERE smc_campaign_id = '{self.smc_campaign_id}'"
        sql2 = insert(table, tuple(data_dic.keys()), tuple(data_dic.values()))
        MA().query([sql1, sql2])
