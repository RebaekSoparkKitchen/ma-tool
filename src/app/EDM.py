'''
@Description: 可执行脚本
@Author: FlyingRedPig
@Date: 2020-05-12 19:44:54
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-23 15:28:44
@FilePath: \MA_tool\src\app\EDM.py
'''
import sys

import fire

sys.path.append("../..")
import time

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

t1 = time.time()
from src.Connector.MA import MA
from src.Controller.TableCreator import create_table

t2 = time.time()
print(t2 - t1)


class EDM(object):

    def __init__(self):
        super().__init__()

    def __pretty(self, df):
        from tabulate import tabulate
        return tabulate(df, headers='keys', tablefmt='psql')

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

    @timer
    def work(self, type: str):
        """
        此命令可以看到我们关心的一系列工作的情况
        future: 未来需完成的工作
        tbd: to be decided, 待定的工作
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

    @timer
    def workflow(self):
        """
        此命令负责跟踪排查我们近期的workflow，包括：未来工作、待定工作、今天需发送报告、哪些条目还没有填写campaign id、我们明天的campaign需要避让哪些campaign
        eg: python edm.py workflow
        """
        self.work('future')
        self.work('tbd')
        self.work('report')
        self.work('campaign_id')
        self.work('limit')

    def write_campaign_id(self):
        '''
        此命令负责检查：今天之前需要发送的edm，是否没有填上SMC campaign id，若没有填上，此方法会提供一些信息，帮助您填写它。
        eg: python edm.py write_campaign_id
        '''

        a = Analytics()

        if a.check().empty:
            return "没啥campaign id需要写啊~"
        for index, row in a.check().iterrows():
            print(row)
            while True:
                campaignId = input('请输入以上campaign的id，谢谢~')
                if campaignId == "next" or "exit":
                    break
                try:
                    int(campaignId)
                    break
                except ValueError:
                    print('请输入正确格式的campaign id')
            if campaignId == "exit":
                print('您已退出campaign_id输入环境')
                break
            elif campaignId == "next":
                continue
            else:
                self.getTrackerInput().writeCampaignId(index, campaignId)
                self.getTrackerInput().saveTracker()
        return

    def report(self, campaignId, catagory="static", path='../../report/'):
        '''
        此命令提供报告生成功能
        eg:  python edm.py report 1234 static
        其中 1234 指SMC campaign id
        static控制是否覆盖已有报告，这个参数只有两个值：static/dynamic，这个值也可以不填，默认为static

        '''
        if self.getMA().readConfig()['username'] == "":
            username = input("此命令将访问数据库，您需要填写username: ")
            self.setting('username', username)
        l = LocalData()  # 此处硬编码了地址，因为脚本文件和类文件不在同一个位置，那么与campaign_data.json的相对位置也不同
        w = WriteTracker()

        if catagory == "static":
            l.request(overwrite=False, campaignId=campaignId)
            s = SqlWriter(campaignId)  # 一定要在这里初始化，因为sqlWriter初始化的时候要在数据库中找这个campaign id 所以必须要上一行代码执行结束之后才行
            s.push(overwrite=False)
        elif catagory == "dynamic":
            l.request(overwrite=True, campaignId=campaignId)
            s = SqlWriter(campaignId)
            s.push(overwrite=True)
        else:
            raise ValueError('catagory参数只接收static或者dynamic')

        r = ReportExcel(
            campaignId)
        r.create(path=path)
        self.getTrackerInput().writePerformanceData(campaignId)
        self.getTrackerInput().saveTracker()
        a = Analytics(campaignId)
        print(f'《{a.name()}》数据报告已创建成功')
        print(f'campaign id: {campaignId}')
        print(f'owner: {a.owner()}')
        print(f'Launch Date: {a.launchDate()}')

        reportInfo = Report(campaignId)
        time = reportInfo.time()
        editor = reportInfo.editor()
        print('报告中的数据由{}创建于{}'.format(editor, time))
        return

    def routine(self):
        '''
        此命令是其他几个命令的大集合（important），每天都需要执行的一个指令，提供信息如：未来工作、今天需发送报告、哪些campaign id需登记等
        '''

        self.workflow()
        self.write_campaign_id()
        a = Analytics()
        reportDf = a.report()
        # the noId / withId crazy staff is to solve bug like campaign id == null in reportDf
        noIdReportDf = reportDf[reportDf['Campaign ID'].isna()]
        withIdReportDf = reportDf[reportDf['Campaign ID'].notna()]
        reportList = list(withIdReportDf['Campaign ID'])
        reportList = list(map(int, reportList))  # 此行重要，df中campaign_id是float形式
        noIdReportList = list(noIdReportDf['Campaign Name'])
        if len(noIdReportList) > 0:
            print("以下campaign应该今天发送报告，但没有campaign id，他们包括：\n{campaign}".format(campaign='\n'.join(noIdReportList)))

        if len(reportList) > 0:
            print('以下campaign应该在今天发送报告')
            for campaignId in reportList:
                self.report(campaignId)

        preReportDf = a.report('20200101', 'yesterday')
        preNoIdReportDf = preReportDf[preReportDf['Campaign ID'].isna()]
        preWithIdReportDf = preReportDf[preReportDf['Campaign ID'].notna()]
        preWithIdReportDf = preWithIdReportDf[preWithIdReportDf['Campaign ID'].apply(
            lambda x: not Report(x).judge())]  # 排除掉数据库中BasicPerformance表中已经有的campaign id
        preReportList = list(preWithIdReportDf['Campaign ID'])
        preReportList = list(map(int, preReportList))  # 此行重要，df中campaign_id是float形式
        preNoIdReportList = list(preNoIdReportDf['Campaign Name'])
        if len(preNoIdReportList) > 0:
            print("以下campaign应该今天以前发送报告，但没有campaign id，他们包括：\n{campaign}".format(campaign='\n'.join(preNoIdReportList)))

        if len(preReportList) > 0:
            print('以下campaign应该在今天以前发送报告')
            for campaignId in preReportList:
                self.report(campaignId)
        # 最后再生成simple_tracker，以便于把刚刚写的campaign id也计算进去
        self.simple_tracker()
        return

    def transfer(self):
        '''
        此命令会弹出数据格式转换的用户界面，请注意我们要求模板为GC_STANDARD_EXPORT_EMAIL,
        不建议其他模板的csv文件转换。
        '''
        t = DataTransfer()
        t.execute()
        return

    def data(self, country: str, time1: int, time2: int):
        '''
        此命令提供一段时间内某一地区的基本数据,并将以excel的形式存在EDM_project/analytics_data中。
        eg: python edm.py data hongkong 20200101 20200630
        '''
        data = DataExtractor()
        data.save(country, str(time1), str(time2))
        return

    def setting(self, attribute: str, data: str):
        '''
        此命令负责更改个人设置，目前仅支持修改用户名，建议只在开始使用时设置一次即可。
        '''
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
