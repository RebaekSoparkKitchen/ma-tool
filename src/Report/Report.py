'''
@Description: 在生成报告的时候显示报告相关的信息, eg: time, editor
@Author: FlyingRedPig
@Date: 2020-08-07 16:11:11
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-07 17:46:33
@FlePath: \EDM\src\Report\Report.py
'''
from src.Control.MA import MA
import sqlite3

class Report(MA):
    def __init__(self, campaignId):
        super().__init__()
        self.campaignId = campaignId

    def __select(self, attribute: str):
        sql = 'SELECT {} FROM BasicPerformance WHERE smc_campaign_id={}'.format(attribute, self.campaignId)
        result = self.sqlProcess(sql)
        return result

    def time(self) -> str:
        result = self.__select('creation_time')
        return result[0][0]

    def editor(self):
        result = self.__select('editor')
        return result[0][0]
    
    



