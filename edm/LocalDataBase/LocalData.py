'''
@Description: 本地数据库需要发起请求，拿到campaign的basic和click performance数据，并主要提供request()和search()两个接口
@Author: FlyingRedPig
@Date: 2020-05-07 16:15:45
@LastEditors: FlyingRedPig
@LastEditTime: 2020-05-13 20:24:36
@FilePath: \EDM\edm\LocalDataBase\LocalData.py
'''
import sys
sys.path.append('../..')

import json
from edm.Spider.BasicPerformance import BasicPerformance
from edm.Spider.ClickPerformance import ClickPerformance
import pandas as pd


class LocalData(object):

    def __init__(self, dataPath="../data/campaign_data.json"):
        '''
        @description: 
        @param {str} 本地数据库的地址 
        @return: 
        '''
        filename = dataPath
        with open(filename) as f_obj:
            self.__data = json.load(f_obj)
        if self.__data is None:
            self.__data = {}
        
        self.__dataPath = dataPath
        self.__configPath = "../config/config.json"

    def getData(self):
        return self.__data
    
    def getDataPath(self):
        return self.__dataPath
    
    def getConfigPath(self):
        return self.__configPath

    def __SMC2Dict(self, campaignId) -> dict:

        
        totalDic = {}
        dic = {}
        basicData = BasicPerformance(campaignId)
        dic['basic_performance'] = basicData.basicPerformanceData()
        clickData = ClickPerformance(campaignId, basicData.driver)
        dic['click_performance'] = clickData.clickPerformanceData()
        totalDic[campaignId] = dic

        return totalDic

    def request(self, overwrite: bool, campaignId: str or int) -> None:

        assert type(overwrite) == bool
        if not overwrite:
            if (str(campaignId) in self.getData()) or (int(campaignId) in self.getData()):
                return
            
        dic = self.__SMC2Dict(campaignId)
            
        self.__data.update(dic)  #若有键值则update新值，若无则添加 
        #!important
        # 千万不要写self.__data = self.__data.update(dic) 会把数据库清零的！！！
        assert type(dic) == dict

        filename = self.getDataPath()
        with open(filename, 'w') as f_obj:
            json.dump(self.getData(), f_obj)

        return

    def search(self, campaignId: int or str):

        campaignId = str(campaignId)
        target = {}
        filename = self.getDataPath()
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

    
    def clickPerformanceDf(self, campaignId:int or str) -> pd.DataFrame :
        '''
        @description:将json中的click_performance转换为dataframe数据结构
        @param {int or str} campaignId 
        @return: pd.DataFrame
        '''
        dic = self.search(campaignId)['click_performance']
        df = pd.DataFrame(dic)
        df['Clicks'] = df['Clicks'].astype(int)
        df = df[df['Clicks']>0]
        df.sort_values(by="Clicks", inplace=True, ascending=False)
        df.reset_index(drop=True)
        return df[['Content Link Name','Clicks']]

    def otherLink(self):
        
        f = open(self.getConfigPath(),encoding="utf-8")
        configDic = json.load(f)
        return configDic['other_link']

    def mainClickPerformanceDf(self, campaignId:int or str) -> pd.DataFrame :
        
        df = self.clickPerformanceDf(campaignId)
        df = df[df['Content Link Name'].apply(lambda x: x not in self.otherLink())]
        df.rename(columns={'Content Link Name':'Main Link Name', 'Clicks':'Click Numbers'}, inplace=True)
        df.reset_index(drop=True)
        return df
    
    def otherClickPerformanceDf(self, campaignId:int or str) -> pd.DataFrame :
        
        df = self.clickPerformanceDf(campaignId)
        df = df[df['Content Link Name'].apply(lambda x: x in self.otherLink())]
        df.rename(columns={'Content Link Name':'Other Link Name', 'Clicks':'Click Numbers'}, inplace=True)
        df.reset_index(drop=True)
        return df

    


if __name__ == "__main__":
    l = LocalData(dataPath="../../data/campaign_data.json")
    # l.request(True, 6414)
    # print(l.metricOpenRate(6414))
    # print(l.metricOpen(6414))
    print(l.mainClickPerformanceDf(6867))
    print(l.otherClickPerformanceDf(6867))
    # print('6867' in l.getData())
    # print(l.getData())
    # l.request(False,6867)
    l.search(4227)

