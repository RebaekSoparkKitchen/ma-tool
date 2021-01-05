"""
@Description: 在生成报告的时候显示报告相关的信息, eg: time, editor
@Author: FlyingRedPig
@Date: 2020-08-07 16:11:11
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-23 12:03:51
@FlePath: \EDM\src\Report\Report.py
"""
import sys
sys.path.append("../..")
from src.Connector.MA import MA


class Report(MA):
    def __init__(self, campaignId):
        super().__init__()
        self.campaignId = campaignId

    def __select(self, attribute: str):
        sql = 'SELECT {} FROM BasicPerformance WHERE smc_campaign_id={}'.format(attribute, self.campaignId)
        result = self.sqlProcess(sql)
        return result

    def judge(self):
        """
        judge if a campaign id is already in the database
        true: in the database
        flase: not in the database
        """
        sql = 'SELECT count(*) FROM BasicPerformance WHERE smc_campaign_id={}'.format(self.campaignId)
        result = self.sqlProcess(sql)
        return result[0][0] == 1

    def time(self) -> str:
        result = self.__select('creation_time')
        return result[0][0]

    def editor(self):
        result = self.__select('editor')
        return result[0][0]
    

if __name__ == "__main__":
    a = Report(4227.0)
    print(a.judge())



