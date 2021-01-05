import sys

sys.path.append('../..')
from src.Connector.MA import MA
from src.Utils.SqlHelper import insert
import datetime as dt


class ClickPerformance(object):

    def __init__(self, data: dict):
        self.smc_campaign_id = data['smc_campaign_id']
        self.link_name = data['link_name']
        self.click_number = data['click_number']
        self.link_alias = data['link_alias']
        self.if_main_link = data['if_main_link']

    @staticmethod
    def select(smc_campaign_id):
        sql = f"select * from ClickPerformance where smc_campaign_id = {smc_campaign_id}"
        rows = MA().query(sql, as_dict=True)
        return list(map(ClickPerformance, rows))

    def update(self):
        """
        类似于orm,这一个对象象征着ClickPerformance中的一行，对这一行进行更新
        :return:
        """
        table = 'ClickPerformance'
        data_dic = self.__dict__
        data_dic['editor'] = MA().read_config()['username']
        data_dic['creation_time'] = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S')
        sql1 = f"DELETE FROM ClickPerformance WHERE smc_campaign_id = '{self.smc_campaign_id}' and link_name = '" \
               f"{self.link_name}'"
        sql2 = insert(table, tuple(data_dic.keys()), tuple(data_dic.values()))
        MA().query([sql1, sql2])


if __name__ == '__main__':
    records = {'smc_campaign_id': 0, 'link_name': 'new', 'click_number': 250, 'link_alias': 3, 'if_main_link': 4}
    c = ClickPerformance(records)
    r = ClickPerformance.select(4227)
    print(r[1].link_name)
    print(r[1].click_number)
