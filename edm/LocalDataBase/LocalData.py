'''
@Description: 本地数据库需要发起请求，拿到campaign的basic和click performance数据
@Author: FlyingRedPig
@Date: 2020-05-07 16:15:45
@LastEditors: FlyingRedPig
@LastEditTime: 2020-05-07 16:48:51
@FilePath: \EDM\edm\LocalDataBase\LocalData.py
'''
import json
import sys
sys.path.append("..")
from Spider.BasicPerformance import BasicPerformance
from Spider.ClickPerformance import ClickPerformance


class LocalData(object):

    def __init__(self, *args):
        '''
        @description: 
        @param {int / str tuple} 
        @return: 
        '''
        self.campaignId = list(map(int, args))

    def singleSave(self, campaignId: int) -> None:

        dic = {}
        basicData = BasicPerformance(campaignId)
        dic['basic_performance'] = basicData.basicPerformanceData()
        clickData = ClickPerformance(campaignId, basicData.driver)
        dic['click_performance'] = clickData.clickPerformanceData()

        return dic


if __name__ == "__main__":
    l = LocalData(6414)
    print(l.singleSave(6414))
