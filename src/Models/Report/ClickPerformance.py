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
    def valid_click_number(smc_campaign_id):
        click_data_list = ClickPerformance.select(smc_campaign_id)
        valid_click = 0
        for item in click_data_list:
            if item.link_name not in MA().read_config()['other_link']:
                valid_click += int(item.click_number)
        return valid_click

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

    @staticmethod
    def main_link_list(smc_campaign_id):
        link_list = ClickPerformance.select(smc_campaign_id)
        main_list = list(filter(lambda x: x.if_main_link == 1, link_list))
        main_list.sort(key=lambda x: int(x.click_number), reverse=True)
        return main_list

    @staticmethod
    def other_link_list(smc_campaign_id):
        link_list = ClickPerformance.select(smc_campaign_id)
        other_list = list(filter(lambda x: x.if_main_link == 0, link_list))
        # check if click number are numbers rather than string
        other_list = list(filter(lambda x: isinstance(x.click_number, int) or x.isdigit(), other_list))
        other_list.sort(key=lambda x: int(x.click_number), reverse=True)
        return other_list


if __name__ == '__main__':
    a = ClickPerformance.other_link_list(6414)
    for i in a:
        print(i.link_name)
        print(i.click_number)
