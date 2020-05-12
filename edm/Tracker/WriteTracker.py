'''
@Description: 提供所有向tracker中写入的服务
@Author: FlyingRedPig
@Date: 2020-05-12 13:46:11
@LastEditors: FlyingRedPig
@LastEditTime: 2020-05-12 19:57:45
@FilePath: \EDM\edm\Tracker\WriteTracker.py
'''
import sys
sys.path.append('../..')
import openpyxl
from edm.Tracker.RequestTracker import Request_Tracker
from edm.LocalDataBase.LocalData import LocalData

class WriteTracker(Request_Tracker):
    def __init__(self):
        super().__init__()
        self.trackerWb = openpyxl.load_workbook(self.getTrackerPath())
        self.trackerWs = self.trackerWb.active

    def writeCampaignId(self, index:int, campaignId:int or str) -> None:
        '''
        @description: 给定df的索引和campaignId，即可写入对应的campaignID
        @index: df对应的索引； campaignId: 对应即将写入的campaignId，会要求用户输入
        @return: 
        '''
        campaignIdCol = 'K'
        rowNum = index + 2 # 2指openpyxl的行号和dataframe的索引天然的差值
        self.trackerWs[campaignIdCol + str(rowNum)] = campaignId
        return
    
    def writePerformanceData(self, campaignId):
        
        colDic = {'Sent':'R', 'Delivered':'S', 'Opened':'T', 'Soft Bounces':'U', 'Hard Bounces':'V', 'Click':'W', 'Unique Click':'X'}
        
        df = self.getVanillaDf()
        index = df[df['Campaign ID'] == campaignId].index[-1]
        rowNum = index + 2
        data = LocalData().search(campaignId)['basic_performance']
        for item in colDic:
            try:
                self.trackerWs[colDic[item] + str(rowNum)] = data[item]
            except KeyError:   #这个地方是为了避免出现两个词典，key不一样的情况，比如我有communication limit这个key，但爬下来的数据是没有的
                continue
        return

    def saveTracker(self):
        while True:
            try:
                self.trackerWb.save(self.getTrackerPath())
                break
            except PermissionError:
                reminder = input('请关闭RequestTracker，是否现在重试？(y/n)')
                if reminder.lower() == 'y':
                    continue
                elif reminder.lower() == 'n':
                    print('由于您执意不肯关闭RequestTracker，我们无法保存，抱歉！')
                    break
                else:
                    print('请输入正确的命令(y/n)')
        return

        
    if __name__ == "__main__":
        pass
