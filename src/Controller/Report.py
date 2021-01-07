from src.Connector.MA import MA
from src.Models.Report.BasicPerformance import BasicPerformance as ReBasic
from src.Models.Report.ClickPerformance import ClickPerformance as ReClick
from src.Models.Report.ReportData import ReportData
from src.Spider.BasicPerformance import BasicPerformance as SpBasic
from src.Spider.ClickPerformance import ClickPerformance as SpClick
from src.Views.ReportExcel import ReportExcel


class Report(object):

    def __init__(self, smc_campaign_id):
        self.smc_campaign_id = smc_campaign_id

    def update(self):
        """
        api
        实际上包含两个过程 pull & push
        pull : 封装在了data()中，spider的两个类负责
        push : 封装在了update()中，Models.report 中的两个类负责
        :return:
        """
        basic, click = self.gen_data()
        click_performance_list = list(map(ReClick, click))
        # 执行顺序最为重要，basic的valid click要从ClickPerformance里面提数据
        for item in click_performance_list:
            item.update()
        ReBasic(basic).update()

    def to_excel(self, path: str = ''):
        r = ReportExcel(self.smc_campaign_id)
        r.save(path)

    def gen_data(self):
        """
        an intermediate treatment for basic_performance between Spider and Report
        :return:
        """
        b = SpBasic(self.smc_campaign_id)
        basic_data_dic = b.data()
        c = SpClick(self.smc_campaign_id, b.driver)
        click_data_list = c.data()
        basic_data_dic = self.change_basic_key(basic_data_dic)
        click_data_list = list(map(self.change_click_key, click_data_list))
        return basic_data_dic, click_data_list

    @staticmethod
    def change_basic_key(data_dic):
        data_dic['sent'] = data_dic.pop('Sent')
        data_dic['hard_bounces'] = data_dic.pop('Hard Bounces')
        data_dic['soft_bounces'] = data_dic.pop('Soft Bounces')
        data_dic['delivered'] = data_dic.pop('Delivered')
        data_dic['opened'] = data_dic.pop('Opened')
        data_dic['unique_click'] = data_dic.pop('Unique Click')
        data_dic['click'] = data_dic.pop('Click')
        return data_dic

    def is_exist(self):
        return ReportData.query_campaign_id(self.smc_campaign_id)

    @staticmethod
    def change_click_key(data_dic):
        data_dic['click_number'] = data_dic.pop('Clicks')
        data_dic['link_name'] = data_dic.pop('Content Link Name')
        data_dic['link_alias'] = data_dic.pop('Link Alias')
        other_link = MA().read_config()['other_link']
        if data_dic['link_name'] in other_link:
            data_dic['if_main_link'] = 0
        else:
            data_dic['if_main_link'] = 1
        return data_dic


if __name__ == '__main__':
    a = ReportUploader(6414)
    a.upload()
    # b = ReClick.select(6414)
    # c = ReBasic.select(6414)
    # print(b[0].__dict__)
    # print(c.__dict__)
