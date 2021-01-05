"""
@Description: @Description: Request_Tracker类，顾名思义，是对Request Tracker的excel表格建模。
            但此类本身并不进行数据筛选展示也不进行写入操作，只是提供数据清洗，
            并从内部唯一接受path入口读取excel，作为父类存在。
@Author: FlyingRedPig
@Date: 2020-04-30 18:03:27
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-07 16:04:19
@FilePath: \EDM\src\Tracker\RequestTracker.py
"""

import pandas as pd
import datetime as dt
import warnings
from pandas.core.common import SettingWithCopyWarning
from src.Connector.MA import MA


class Request_Tracker(MA):

    def __init__(self, *args):
        
        super().__init__()
        self.__path = self.readConfig()['data_location']['RequestTracker']
        self.__vanillaDf = pd.read_excel(self.__path, encoding='utf-8')
        self.__cleanDf = self.cleanDate()
        self.__campaignId = args

    def getVanillaDf(self):
        return self.__vanillaDf

    def getCleanDf(self):
        return self.__cleanDf

    def getCampaignId(self):
        return self.__campaignId

    def setCampaignId(self, *args):
        self.__campaignId = args

    def getTrackerPath(self):
        return self.__path

    def __transDate(self, x):
        """
        辅助函数，从excel读成dataframe的时候是时间戳，需要转换为time.date类型
        这个函数的精彩之处在于：能转date类型转过去，转不过去的仍保留原值，这就使"待定" "取消"等词得以保留
        """

        try:
            return x.date()
        except AttributeError:
            return x

    def turnWeekday(self, x):
        """
        help function
        根据日期添加星期一列
        """
        dic = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期日',
        }

        try:
            return dic[x.weekday()]
        except AttributeError:
            return None

    def cleanDate(self):
        """
        input: self.vanillaDf 
        output: self.cleanDf

        """
        warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
        # 此函数会报 pandas warning: SettingWithCopyWaring, 经查证，这是一个pandas的bug
        # 即：foo = df['Launch Date']
        #     foo['Weekday'] = 'Mon'
        # 形如此类则会被判断为此Warning，文档声称这是设计中的一个bug

        df = self.getVanillaDf()  # 获取数据

        for col in ['Launch Date', 'Event Date', 'Report Date']:
            df[col] = df[col].apply(
                lambda x: self.__transDate(x))  #把涉及时间的列转换为date类型

        df = df[df['Launch Date'].apply(
            lambda x: isinstance(x, dt.date))]  #待定 取消等词均被删掉，只留下有Lauch Date日期的行
        df['Weekday'] = df['Launch Date'].apply(lambda x: self.turnWeekday(x))

        return df


if __name__ == '__main__':

    r = Request_Tracker(6140)
