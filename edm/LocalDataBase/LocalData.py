'''
@Description: 本地数据库需要发起请求，拿到campaign的basic和click performance数据，并主要提供save()和search()两个接口
@Author: FlyingRedPig
@Date: 2020-05-07 16:15:45
@LastEditors: FlyingRedPig
@LastEditTime: 2020-05-10 13:18:28
@FilePath: \EDM\edm\LocalDataBase\LocalData.py
'''
import json
import sys
sys.path.append('../Spider')
from BasicPerformance import BasicPerformance
from ClickPerformance import ClickPerformance


class LocalData(object):

    def __init__(self):
        '''
        @description: 
        @param {int / str tuple} 
        @return: 
        '''
        filename = '../../data/campaign_data.json'
        with open(filename) as f_obj:
            self.__data = json.load(f_obj)
        if self.__data is None:
            self.__data = {}

    def getData(self):
        return self.__data

    def __SMC2Dict(self, *args) -> dict:

        campaignId = list(map(int, args))
        totalDic = {}
        for campaign in campaignId:
            dic = {}
            basicData = BasicPerformance(campaign)
            dic['basic_performance'] = basicData.basicPerformanceData()
            clickData = ClickPerformance(campaign, basicData.driver)
            dic['click_performance'] = clickData.clickPerformanceData()
            totalDic[campaign] = dic

        return totalDic

    def save(self, overwrite: bool, *args):

        assert type(overwrite) == bool
        if not overwrite:
            campaignList = []
            for campaign in args:
                if str(campaign) not in self.getData().keys():
                    campaignList.append(campaign)
            args = tuple(campaignList)

        dic = self.__SMC2Dict(*args)
        self.__data.update(dic)  #若有键值则update新值，若无则添加

        filename = '../../data/campaign_data.json'
        with open(filename, 'w') as f_obj:
            json.dump(self.getData(), f_obj)

        return

    def search(self, campaignId: int or str):

        campaignId = str(campaignId)
        target = {}
        filename = '../../data/campaign_data.json'
        with open(filename) as f_obj:
            dic = json.load(f_obj)

        return dic[campaignId]

    def length(self):
        return len(self.__data)

    def metricDeliver(self, campaignId: int or str) -> int:
        return self.search(campaignId)['basic_performance']['Delivered']

    def metricSent(self, campaignId: int or str) -> int:
        return self.search(campaignId)['basic_performance']['Sent']

    def metricOpen(self, campaignId: int or str) -> int:
        return self.search(campaignId)['basic_performance']['Opened']

    def metricClick(self, campaignId: int or str) -> int:
        return self.search(campaignId)['basic_performance']['Click']

    def metricUniqueClick(self, campaignId: int or str) -> int:
        return self.search(campaignId)['basic_performance']['Unique Click']

    def metricOpenRate(self, campaignId: int or str) -> float:
        return self.metricOpen(campaignId) / self.metricDeliver(campaignId)

    def metricCTR(self, campaignId: int or str) -> float:
        return self.metricClick(campaignId) / self.metricDeliver(campaignId)

    def metricClickToOpen(self, campaignId: int or str) -> float:
        return self.metricUniqueClick(campaignId) / self.metricOpen(campaignId)


if __name__ == "__main__":
    l = LocalData()
    # l.save(True, 6414)
    print(l.metricOpenRate(6414))
    print(l.metricOpen(6414))
