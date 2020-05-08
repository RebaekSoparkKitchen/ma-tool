'''
@Description: 此类负责report的excel表格的内容及排版
@Author: FlyingRedPig
@Date: 2020-05-08 11:35:14
@LastEditors: FlyingRedPig
@LastEditTime: 2020-05-08 14:47:44
@FilePath: \EDM\edm\Report\ReportExcel.py
'''
from openpyxl.styles import Font, colors, Alignment, PatternFill, Border, Side
import openpyxl
import sys
sys.path.append('../LocalDataBase')
from LocalData import LocalData


class ReportExcel():

    def __init__(
        self,
        campaignId,
        templatePath=r'C:\Users\C5293427\Desktop\MA\Report_template.xlsx'):
        self.reportWb = openpyxl.load_workbook(templatePath)
        self.reportWs = self.reportWb.active
        self.campaignId = campaignId

    def getCampaignId(self):
        return self.campaignId

    def addBasicPerformance(self):

        metricDic = {
            'Sent': 'A4',
            'Delivered': 'B4',
            'Opened': 'C4',
            'Click': 'D4',
            'Unique Click': 'E4'
        }

        db = LocalData()
        dataDic = db.search(self.getCampaignId())['basic_performance']

        for metric in metricDic.keys():
            if metric in dataDic.keys():
                self.reportWs[metricDic[metric]] = dataDic[metric]
            else:
                self.reportWs[metricDic[metric]] = 0
        return

    def save(self):
        self.reportWb.save('testexcel.xlsx')


if __name__ == "__main__":
    r = ReportExcel(6414)
    r.addBasicPerformance()
    r.save()
    # db = LocalData()
    # dataDic = db.search(6414)['basic_performance']
    # print(dataDic)
