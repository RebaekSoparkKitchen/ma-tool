'''
@Description: 
本地数据库需要发起请求，拿到campaign的basic和click performance数据，并主要提供request()和search()两个接口
data flow:
spider -> local_data(raw data) -> sql_computer(中间计算层) -> sql_writer(更完备的记录进入数据库)
                               -> report (只是分发一部分)
                               -> tracker (只是分发一部分)

实际上sql_computer是local_data的子类，它的作用是把数据再包装一下交给sql_writer
所以sql_writer只需要调用sql_computer中的basicData和clickData方法即可得到自己想要的数据了
@Author: FlyingRedPig
@Date: 2020-05-07 16:15:45
@LastEditors: ,: FlyingRedPig
@LastEditTime: ,: 2020-10-21 10:39:34
@FilePath: ,: \MA_tool\src\LocalDataBase\LocalData.py
'''
import sys
sys.path.append('../..')
sys.path.append('../../bin')
sys.path.append('..')

import json
from src.Spider.BasicPerformance import BasicPerformance
from src.Spider.ClickPerformance import ClickPerformance
from src.Control.MA import MA
import pandas as pd


class LocalData(MA):

    def __init__(self):
        '''
        @description: 
        @param {str} 本地数据库的地址 
        @return: 
        '''
        super().__init__()
        filename = self.readConfig()['data_location']['SMCData']
        with open(filename) as f_obj:
            self.__data = json.load(f_obj)
        if self.__data is None:
            self.__data = {}
        
        self.__dataPath = filename

    def getData(self):
        return self.__data
    
    def getDataPath(self):
        return self.__dataPath
    

    def __SMC2Dict(self, campaignId) -> dict:
        '''
        important
        它是localData和spider的一个对接口
        '''
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
        
        # dynamic 情况
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
        '''
        important!
        为其他类提供接口
        '''
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
        if self.metricOpen(campaignId) == 0:
            return 0
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
        return self.readConfig()['other_link']

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
    l = LocalData()
    a = l.search(9728)
    print(a)

