"""
@Description: 可执行脚本
@Author: FlyingRedPig
@Date: 2020-05-12 19:44:54
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-23 15:28:44
@FilePath: \MA_tool\src\app\EDM.py
"""
import sys

import fire

sys.path.append("../..")

# from src.Tracker.Analytics import Analytics
# from src.Tracker.WriteTracker import WriteTracker
# from src.Tracker.Data import DataExtractor
# from src.Spider.BasicPerformance import BasicPerformance
# from src.Spider.ClickPerformance import ClickPerformance
# from src.LocalDataBase.LocalData import LocalData
# from src.LocalDataBase.SqlWriter import SqlWriter
# from src.Report.ReportExcel import ReportExcel
# from src.Report.Report import Report
# from src.Transfer.gui import DataTransfer

from src.Utils.timer import timer
from src.Connector.MA import MA
from src.Controller.TableCreator import create_table


class EDM(object):

    def __init__(self):
        super().__init__()

    @timer
    def simple_tracker(self, days=21):
        """
        此命令负责刷新simple_tracker，是我们需求安排的日程版本，
        您可以在EDM_project/files中找到它。
        """
        from src.Models.SimpleTracker import SimpleTracker
        path = MA().read_config()['file_location']['SimpleTracker']
        s = SimpleTracker(days_diff=days)
        s.main(path=path)
        return

    def work(self, type: str):
        """
        此命令可以看到我们关心的一系列工作的情况
        future: 未来需完成的工作
        tbd: to be determined, 待定的工作
        report: 今天需要发送报告的工作
        campaign id: 今天需要填写smc campaign id的工作
        limit: 明天的campaign需要注意哪些campaign的communication limitation
        """
        import src.Models.Workflow as wf
        if type == 'future':
            create_table(wf.future_work())
        elif type == 'tbd':
            create_table(wf.tbd_work())
        elif type == 'report':
            create_table(wf.report_work())
        elif type == 'campaign_id':
            create_table(wf.campaign_id_work())
        elif type == 'limit':
            create_table(wf.communication_limit_work())
        else:
            print('Your command is not right, should be in [future, tbd, report, campaign_id, limit]')

    def workflow(self):
        """
        此命令负责跟踪排查我们近期的workflow，包括：未来工作、待定工作、今天需发送报告、哪些条目还没有填写campaign id、我们明天的campaign需要避让哪些campaign
        eg: python edm.py workflow
        """
        for command in ['future', 'tbd', 'report', 'campaign_id', 'limit']:
            self.work(command)

    def write_campaign_id(self):
        """
        此命令负责检查：今天之前需要发送的edm，是否没有填上SMC campaign id，若没有填上，此方法会提供一些信息，帮助您填写它。
        eg: python edm.py write_campaign_id
        :return: void
        """
        from src.Controller.CampaignIdUploader import upload
        upload()

    def report(self, smc_campaign_id, category="static", path=''):
        """
        此命令提供报告生成功能
        eg:  python edm.py report 1234 static
        其中 1234 指SMC campaign id
        static控制是否覆盖已有报告，这个参数只有两个值：static/dynamic，这个值也可以不填，默认为static

        """
        assert category in ['static', 'dynamic'], "category参数只接收static或者dynamic"
        from src.Controller.Report import Report
        if MA().read_config()['username'] == "":
            username = input("此命令将访问数据库，您需要填写username: ")
            self.setting('username', username)
        r = Report(smc_campaign_id)
        if category == "static" and r.is_exist():
            r.to_excel(path)
        else:
            r.update()
            r.to_excel(path)
        r.show_introduction()

        return

    def routine(self):
        """
        此命令是其他几个命令的大集合（important），每天都需要执行的一个指令，提供信息如：未来工作、今天需发送报告、哪些campaign id需登记等
        """

        # write today's smc campaign id
        self.write_campaign_id()

        # scan works
        self.workflow()

        # deal with report work
        from src.Models.Workflow import report_work
        r = report_work()
        for item in r.content:
            self.report(item[-1], 'static')

        # generate simple_tracker
        self.simple_tracker()

    def transfer(self):
        """
        此命令会弹出数据格式转换的用户界面，请注意我们要求模板为GC_STANDARD_EXPORT_EMAIL,
        不建议其他模板的csv文件转换。
        """
        from src.Views.Transfer.TransferGui import DataTransfer
        DataTransfer().execute()
        return

    def data(self, country: str, date1: str, date2: str):
        """
        此命令提供一段时间内某一地区的基本数据,并将以excel的形式存在EDM_project/analytics_data中。
        eg: python edm.py data hongkong 20200101 20200630
        """
        from src.Controller.MetricsController import MetricsController

        metrics = MetricsController(country, str(date1), str(date2))
        metrics.export()
        return

    def setting(self, attribute: str, data: str):
        """
        此命令负责更改个人设置，目前仅支持修改用户名，建议只在开始使用时设置一次即可。
        """
        config = self.getMA().readConfig()
        assert attribute == "username"
        self.getMA().setConfig('username', data)
        return

    def request(self, type: str = 'create'):
        """
        此命令负责request的管理，type分为[create, delete, edit, check]
        分别对应增删改查
        """
        from src.Controller.Request import create
        if type == 'create':
            create()
        # elif type == 'delete':
        #     Command.delete()
        # elif type == 'check':
        #     Command.check()
        # elif type == 'edit':
        #     Command.edit()
        pass


if __name__ == "__main__":
    fire.Fire(EDM)
