'''
@Description: 可执行脚本
@Author: FlyingRedPig
@Date: 2020-05-12 19:44:54
@LastEditors: FlyingRedPig
@LastEditTime: 2020-05-12 23:48:05
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
        pass
    
    def simple_tracker(self, path:str = "../../file/"):
        s = SimpleTracker(path)
        s.simpleTrackerExcel()
        print('Simple_tracker.xlsx has been created successfully！')
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
            print('\n过去的campaign都添上了campaign id, 很棒！')
        else:
            print(self.__pretty(a.check()))
        print('\n')

        print('由于traffic control, 我们需要在执行时间上考虑以下campaign:')
        if a.communicationLimitHint().empty:
            print('我们没有时间上的避让考虑')
        else:
            print(self.__pretty(a.communicationLimitHint()))
        
        return

    def write_campaign_id(self):
        
        a = Analytics()
        w = WriteTracker()
        if a.check().empty:
            return "没啥campaign id需要写啊~"
        for index, row in a.check().iterrows():
            print(row)
            campaignId = input('请输入以上campaign的id，谢谢~')
            w.writeCampaignId(campaignId)
            w.saveTracker()
        return
    
    def report(self, overwrite=False, path="../../report/",*args):
        
        l = LocalData()
        l.request(overwrite, *args)
        for campaignId in args:
            r = ReportExcel()
            r.create(path)
        return 
    

if __name__ == "__main__":
    fire.Fire(EDM)
