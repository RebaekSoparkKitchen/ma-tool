'''
@Description: 可执行脚本
@Author: FlyingRedPig
@Date: 2020-05-12 19:44:54
@LastEditors: FlyingRedPig
@LastEditTime: 2020-05-13 20:05:53
@FilePath: \EDM\bin\EDM.py
'''
import fire
import sys
sys.path.append("..")
sys.path.append("../edm/LocalDataBase/")

from edm.Tracker.Analytics import Analytics
from edm.Tracker.SimpleTracker import SimpleTracker
from edm.Tracker.WriteTracker import WriteTracker
from edm.Spider.BasicPerformance import BasicPerformance
from edm.Spider.ClickPerformance import ClickPerformance
from edm.LocalDataBase.LocalData import LocalData
from edm.Report.ReportExcel import ReportExcel

from tabulate import tabulate
import pandas as pd


class EDM(object):

    def __init__(self):
        self.trackerInput = WriteTracker()

    def __getTrackerInput(self):
        return self.trackerInput
    
    def simple_tracker(self, path:str = "../../files/"):
        s = SimpleTracker(path)
        s.simpleTrackerExcel()
        print('Simple_tracker.xlsx 已经创建成功！')
        return 

    def __pretty(self, df):
        return tabulate(df, headers='keys', tablefmt='psql')

    def workflow(self):

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
        
        a = Analytics()
        
        if a.check().empty:
            return "没啥campaign id需要写啊~"
        for index, row in a.check().iterrows():
            print(row)
            while True:
                campaignId = input('请输入以上campaign的id，谢谢~')
                if campaignId =="next" or "exit":
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
        
        l = LocalData(dataPath="../data/campaign_data.json") #此处硬编码了地址，因为脚本文件和类文件不在同一个位置，那么与campaign_data.json的相对位置也不同
        w = WriteTracker()
        if catagory == "static":
            l.request(False, campaignId)
        elif catagory == "dynamic":
            l.request(True, campaignId)
        else:
            raise ValueError('catagory参数只接收static或者dynamic')
        
        r = ReportExcel(campaignId, templatePath="../config/Report_template.xlsx")
        r.create(path=path)
        self.trackerInput.writePerformanceData(campaignId)
        self.trackerInput.saveTracker()
        a = Analytics(campaignId)
        print('《{}》数据报告已创建成功！'.format(a.name()))
        return 
    
    def routine(self):
        
        a = Analytics()

        self.simple_tracker()
        self.workflow()
        self.write_campaign_id()
        reportList = list(a.report()['Campaign ID'])
        reportList = list(map(int, reportList)) #此行重要，df中campaign_id是float形式
       
        for campaignId in reportList:
            self.report(campaignId)
        return 
        

if __name__ == "__main__":
    fire.Fire(EDM)
    
