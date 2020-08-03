'''
@Description: 主要为SqlWriter提供clickData()和basicData()两个接口
@Author: FlyingRedPig
@Date: 2020-08-01 14:23:41
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-03 11:27:20
@FilePath: \EDM\edm\LocalDataBase\SqlComputer.py
'''
import sys
sys.path.append("..")
from edm.LocalDataBase.LocalData import LocalData
import datetime


class SqlComputer(LocalData):

    def __init__(self, campaignId):
        super().__init__()
        self.__campaignId = campaignId
        self.__rawData = self.pull()
        self.__click = self.clickData() #由于此方法在本类中多个方法调用，索性直接初始化时就做一次存起来
        self.__basic = self.basicData()

    def getCampaignId(self):
        return self.__campaignId
    
    def getClick(self):
        return self.__click
    
    def getBasic(self):
        return self.__basic
    
    def pull(self) -> dict:
        '''
        local_data中的json数据流向了我们这个子类
        '''
        try:
            return self.search(self.__campaignId)
        except KeyError:
            self.request(overwrite=True, campaignId=self.__campaignId)
            return self.search(self.__campaignId)


    def __otherLinkList(self) -> list:
        config = self.readConfig()
        return config['other_link']

    def __checkMainLink(self,x:str) -> int:
        '''
        0 -> False
        1 -> True
        '''
        if x in self.__otherLinkList():
            return 0
        return 1
    

    def clickData(self) -> list:
        '''
        此方法提供数据给到sql table: click_performance
        '''
        data = self.__rawData['click_performance']
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 新增三个json文件中没有的数据维度
        for row in data:
            row['smc_campaign_id'] = self.__campaignId
            row['creation_time'] = nowTime
            row['if_main_click'] = self.__checkMainLink(row['Content Link Name'])
            if 'Link Alias' not in row.keys(): #历史遗留问题，link_alias是后加的一个attribute
                row['Link Alias'] = ''
        return data

    def linkNum(self) -> int: 
        return len(self.__click)

    def mainLinkNum(self) -> int:
        data = self.__click
        num = 0
        for item in data:
            if item['if_main_click'] == 1:
                num += 1
        return num
    
    def otherLinkNum(self) -> int:
        data = self.__click
        num = 0
        for item in data:
            if item['if_main_click'] == 0:
                num += 1
        return num
    
    def validClickNum(self):
        data = self.__click
        num = 0
        for item in data:
            if item['if_main_click'] == 1:
                num += int(item['Clicks'])
        return num
    
    def otherClickNum(self):
        data = self.__click
        num = 0
        for item in data:
            if item['if_main_click'] == 0:
                num += int(item['Clicks'])
        return num

    def basicData(self) -> list:
        '''
        此方法提供数据给到sql table: basic_performance
        '''
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = self.__rawData['basic_performance']
        clickData = self.__click
        data['creation_time'] = nowTime
        data['smc_campaign_id'] = self.__campaignId
        data['main_link_num'] = self.mainLinkNum()
        data['other_link_num'] = self.otherLinkNum()
        data['link_num'] = self.linkNum()
        data['valid_click'] = self.validClickNum()
        data['other_click'] = self.otherClickNum()
        data['bounce_rate'] = (data['Hard Bounces'] + data['Soft Bounces']) / data['Sent']
        data['open_rate'] = data['Opened'] / data['Delivered']
        data['unique_click_to_open_rate'] = data['Unique Click'] / data['Opened']
        data['valid_click_to_open_rate'] = data['valid_click'] / data['Opened']
        data['vanilla_click_to_open_rate'] = data['Click'] / data['Opened']
        data['ctr'] = data['Click'] / data['Delivered']
        data['unique_ctr'] = data['Unique Click'] / data['Delivered']
        return data
        
    
