'''
@Description: 此类负责report的excel表格的内容及排版
@Author: FlyingRedPig
@Date: 2020-05-08 11:35:14
@LastEditors: FlyingRedPig
@LastEditTime: 2020-05-10 13:23:44
@FilePath: \EDM\edm\Report\ReportExcel.py
'''
from openpyxl.styles import Font, colors, Alignment, PatternFill, Border, Side
import openpyxl
import sys
sys.path.append('../LocalDataBase')
sys.path.append('../Tracker')
from LocalData import LocalData
from Analytics import Analytics


class ReportExcel():

    def __init__(
        self,
        campaignId,
        templatePath=r'C:\Users\C5293427\Desktop\MA\Report_template.xlsx'):
        self.reportWb = openpyxl.load_workbook(templatePath)
        self.reportWs = self.reportWb.active
        self.campaignId = campaignId
        self.trackerData = Analytics(self.getCampaignId())
        self.localData = LocalData()

    def getCampaignId(self) -> int:
        return int(self.campaignId)

    def getTrackerData(self) -> Analytics:
        return self.trackerData

    def getLocalData(self) -> LocalData:
        return self.localData

    def addName(self) -> None:
        trackerData = self.getTrackerData()
        self.reportWs['A1'] = trackerData.name()
        return

    def addOverview(self) -> None:
        '''
        @description: 这边的接口设计是，所有计算均在对应的RequestTracker和LocalData类中完成，以降低耦合度。
        @param {type} 
        @return: 修改excel对象，添加overview一栏，
        '''

        trackerData = self.getTrackerData()
        localData = self.getLocalData()

        executionTime = trackerData.executionTime()

        openRate = "%.2f%%" % (
            localData.metricOpenRate(self.getCampaignId()) * 100)
        ctr = "%.2f%%" % (localData.metricCTR(self.getCampaignId()) * 100)
        clickToOpen = "%.2f%%" % (
            localData.metricClickToOpen(self.getCampaignId()) * 100)

        timeStr = "\n- Date of execution: 08:00 AM on {}".format(executionTime)
        openRateStr = "\n- Open Rate - {} （GC benchmark: 4-6%）".format(openRate)
        ctrStr = "\n- CTR - {}  (GC benchmark: 0.2 – 0.4 %)".format(ctr)
        clickToOpenStr = "\n- Click-to-open Rate - {} (GC benchmark: 5 - 7 % )".format(
            clickToOpen)
        self.reportWs[
            'A2'] = 'Summary:' + timeStr + openRateStr + ctrStr + clickToOpenStr
        return

    def addBasicPerformance(self) -> None:
        '''
        @description: 添加基本表现信息，这些信息都是从localdata得到的，所以特意从localdata做了接口传过来。
        @param {type} 
        @return: 
        '''
        LocalData = self.getLocalData()

        self.reportWs['A4'] = LocalData.metricSent(self.getCampaignId())
        self.reportWs['B4'] = LocalData.metricDeliver(self.getCampaignId())
        self.reportWs['C4'] = LocalData.metricOpen(self.getCampaignId())
        self.reportWs['D4'] = LocalData.metricClick(self.getCampaignId())
        self.reportWs['E4'] = LocalData.metricUniqueClick(self.getCampaignId())

        return

    def save(self):
        self.reportWb.save('testexcel.xlsx')


if __name__ == "__main__":
    r = ReportExcel(6414)
    r.addBasicPerformance()
    r.addName()
    r.addOverview()
    r.save()
    # db = LocalData()
    # dataDic = db.search(6414)['basic_performance']
    # print(dataDic)
