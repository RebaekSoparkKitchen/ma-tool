'''
@Description: Request_Tracker类，顾名思义，是对Request Tracker的excel表格建模。
            但此类本身并不进行数据筛选展示也不进行写入操作，只是提供数据清洗，
            并从内部唯一接受path入口读取excel，作为父类存在。
@Author: FlyingRedPig
@Date: 2020-04-23 10:31:20
@LastEditors: FlyingRedPig
@LastEditTime: 2020-04-23 12:12:28
@FilePath: \edm\RequestTracker.py
'''

import pandas as pd
import datetime as dt
import warnings


class Request_Tracker(object):


    def __init__(self, *args):

        self.__path = r'C:\Users\C5293427\Desktop\MA\Request_Tracker.xlsx'
        self.__vanillaDf = pd.read_excel(self.__path, encoding = 'utf-8')
        self.__cleanDf = self.cleanDate()
        self.__campaignId = args

    def getVanilladf(self):
        return self.__vanillaDf

    def getCleanDf(self):
        return self.__cleanDf

    def getCampaignId(self):
        return self.__campaignId

    def setCampaignId(self, *args):
        self.__campaignId = args


    def __transDate(self, x):
        '''
        辅助函数，从excel读成dataframe的时候是时间戳，需要转换为time.date类型
        这个函数的精彩之处在于：能转date类型转过去，转不过去的仍保留原值，这就使"待定" "取消"等词得以保留
        '''
        try:
            return x.date()
        except AttributeError:
            return x


    def __turnWeekday(self, x):
        '''
        help function
        根据日期添加星期一列
        '''
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
        '''
        input: self.vanillaDf 
        output: self.cleanDf

        '''
        warnings.filterwarnings('ignore') 
        # 此函数会报 pandas warning: SettingWithCopyWaring, 经查证，这是一个pandas的bug 
        # 即：foo = df['Launch Date']
        #     foo['weekday'] = 'Mon'
        # 形如此类则会被判断为此Warning，文档声称这是设计中的一个bug
    
        df = self.getVanilladf()  # 获取数据

        for col in ['Launch Date', 'Event Date', 'Report Date']:
            df[col] = df[col].apply(lambda x: self.__transDate(x))   #把涉及时间的列转换为date类型
             
        df = df[df['Launch Date'].apply(lambda x: isinstance(x, dt.date))]   #待定 取消等词均被删掉，只留下有Lauch Date日期的行
        df['weekday'] = df['Launch Date'].apply(lambda x: self.__turnWeekday(x))

        return df

    


if __name__ == '__main__':
    t_path = r'C:\Users\C5293427\Desktop\MA\Request_Tracker.xlsx'
    r = Request_Tracker(t_path, 6140)
    print(r.getCleanDf())
    print(len(r.getCampaignId()))
    #print(df['Event Date'].max())

