'''
@Description: 可执行脚本
@Author: FlyingRedPig
@Date: 2020-05-12 19:44:54
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-03 16:47:19
@FilePath: \EDM\bin\EDM.py
'''
import fire
import sys
sys.path.append("..")

from edm.Tracker.Analytics import Analytics
from edm.Tracker.SimpleTracker import SimpleTracker
from edm.Tracker.WriteTracker import WriteTracker
from edm.Tracker.Data import DataExtractor
from edm.Spider.BasicPerformance import BasicPerformance
from edm.Spider.ClickPerformance import ClickPerformance
from edm.LocalDataBase.LocalData import LocalData
from edm.LocalDataBase.SqlWriter import SqlWriter
from edm.Report.ReportExcel import ReportExcel
from edm.Transfer.gui import DataTransfer
from dateutil.parser import parse
from tabulate import tabulate
import pandas as pd
import datetime as dt
from edm.Control.MA import MA


class EDM(MA):

    def __init__(self):
        super().__init__()
        self.trackerInput = WriteTracker()

    def __getTrackerInput(self):
        return self.trackerInput
    
    def __pretty(self, df):
        return tabulate(df, headers='keys', tablefmt='psql')

    def simple_tracker(self, path=None):
        '''
        此命令负责刷新simple_tracker，是我们需求安排的日程版本，
        您可以在EDM_project/files中找到它。
        '''
        if path == None:
            path = self.readConfig()['location']['SimpleTracker']
        s = SimpleTracker(path)
        s.simpleTrackerExcel()
        return

    def workflow(self):
        '''
        此命令负责跟踪排查我们近期的workflow，包括：未来工作、待定工作、今天需发送报告、哪些条目还没有填写campaign id、我们明天的campaign需要避让哪些campaign
        eg: python edm.py workflow
        '''
        a = Analytics()

        print('\n')
        print('我们未来的工作')
        if a.futureWork().empty:
            print('\n据我所知，未来我们没有任何需求')
        else:
            print(self.__pretty(a.futureWork()))
        print('\n')

        print('待定的工作：')
        if a.waitWork().empty:
            print('\n我们没有待定的需求')
        else:
            print(self.__pretty(a.waitWork()))
        print('\n')

        print('今天需要发送的报告：')
        if a.report().empty:
            print('\n今天没有报告要发哈~')
        else:
            print(self.__pretty(a.report()))
        print('\n')

        print('我们需要检查的campaign:')
        if a.check().empty:
            print('\n过去的campaign都填上了campaign id, 很棒！')
        else:
            print(self.__pretty(a.check()))
        print('\n')

        print('由于traffic control, 我们需要在执行时间上考虑以下campaign:')
        if a.communicationLimitHint().empty:
            print('\n我们没有时间上的避让考虑')
        else:
            print(self.__pretty(a.communicationLimitHint()))

        return

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
                self.trackerInput.writeCampaignId(index, campaignId)
                self.trackerInput.saveTracker()
        return

    def report(self, campaignId, catagory="static", path='../../report/'):
        '''
        此命令提供报告生成功能
        eg:  python edm.py report 1234 static
        其中 1234 指SMC campaign id
        static控制是否覆盖已有报告，这个参数只有两个值：static/dynamic，这个值也可以不填，默认为static
         
        '''
        if self.readConfig()['username'] == "":
            username = input("此命令将访问数据库，您需要填写username: ")
            self.setting('username', username)
        l = LocalData()  #此处硬编码了地址，因为脚本文件和类文件不在同一个位置，那么与campaign_data.json的相对位置也不同
        w = WriteTracker()
        
        if catagory == "static":
            l.request(overwrite=False, campaignId=campaignId)
            s = SqlWriter(campaignId)  #一定要在这里初始化，因为sqlWriter初始化的时候要在数据库中找这个campaign id 所以必须要上一行代码执行结束之后才行
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
        self.trackerInput.writePerformanceData(campaignId)
        self.trackerInput.saveTracker()
        a = Analytics(campaignId)
        print('《{}》数据报告已创建成功！'.format(a.name()))
        return

    def routine(self):
        '''
        此命令是其他几个命令的大集合（important），每天都需要执行的一个指令，提供信息如：未来工作、今天需发送报告、哪些campaign id需登记等
        '''

        a = Analytics()

        self.simple_tracker()
        self.workflow()
        self.write_campaign_id()
        reportList = list(a.report()['Campaign ID'])
        reportList = list(map(int, reportList))  #此行重要，df中campaign_id是float形式

        for campaignId in reportList:
            self.report(campaignId)
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
        config = self.readConfig()
        assert attribute == "username"
        self.setConfig('username', data)
        return

    

if __name__ == "__main__":
    fire.Fire(EDM)
    
   