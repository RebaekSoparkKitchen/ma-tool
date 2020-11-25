'''
@Description: Analytics是非常重要的类，它是继承于RequestTracker，为report以及界面展示提供服务
@Author: FlyingRedPig
@Date: 2020-04-30 18:03:27
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-25 13:55:44
@FilePath: \MA_tool\src\Tracker\Analytics.py
'''
import sys
sys.path.append("../..")
import warnings
from dateutil.parser import parse, _parser
import datetime as dt
from src.Tracker.RequestTracker import Request_Tracker

from pandas import Series, DataFrame
import numpy as np
import pandas as pd



class Analytics(Request_Tracker):

    def __init__(self, *args):

        super(Analytics, self).__init__(*args)
        currentYear = dt.datetime.now().year
        df = self.getCleanDf()
        self.__startDate = dt.date(currentYear, 1, 1)
        self.__ytdData = df[df['Launch Date'] > self.__startDate]

    def setStartDate(self, startDate: dt.date):
        if isinstance(startDate, dt.date):
            self.__startDate = startDate
        else:
            raise TypeError("操作无效，请提供datetime.date类型的对象")
        return

    def getStartDate(self):
        return self.__startDate

    def getYtdData(self):
        return self.__ytdData

    def __turnWeekday(self, x):
        '''
        help function
        '''
        try:
            return x.weekday()
        except AttributeError:
            return np.nan

    def futureWork(self):

        df = self.getCleanDf()

        today = dt.date.today()  # 获取此时此刻的时间
        df = df[(df['Launch Date'] > today)]  # 按时间筛选出今天以后的时间
        df = df.sort_values(by='Launch Date')  # 按顺序排列

        if df.empty == True:
            return "There's no campaign in the future"
        return df[[
            'Campaign Name', 'Owner ', 'Launch Date', 'Weekday', 'Event Date'
        ]]

    def report(self, *args):
        '''
        @description: report方法给出我们需要今天report的dataframe
        @param {df:DataFrame, *args:str} *args代表
        @return: DataFrame
        '''

        df = self.getCleanDf()

        # 必须让类型统一，把launch Date中的字符串删掉
        df.loc[df['Launch Date'].apply(lambda x: isinstance(x, str)),
               'Launch Date'] = np.nan

        df['formal report date'] = df['Report Date']

        df.loc[df['Report Date'].isna() & df['Event Date'].isna()
               & df['Launch Date'].isna(), ['formal report date']] = np.nan
        df.loc[df['Report Date'].isna() & df['Event Date'].isna()
               & df['Launch Date'].notna(),
               ['formal report date']] = df['Launch Date'] + dt.timedelta(
                   days=7)
        df.loc[df['Report Date'].isna() & df['Event Date'].notna()
               & df['Launch Date'].isna(), ['formal report date']] = np.nan
        df.loc[df['Report Date'].isna() & df['Event Date'].notna()
               & df['Launch Date'].notna()
               & (df['Event Date'] - df['Launch Date'] > dt.timedelta(days=7)),
               ['formal report date']] = df['Launch Date'] + dt.timedelta(
                   days=7)
        df.loc[df['Report Date'].isna() & df['Event Date'].notna()
               & df['Launch Date'].notna()
               & (df['Event Date'] - df['Launch Date'] <= dt.timedelta(days=7)),
               ['formal report date']] = df['Event Date'] - dt.timedelta(days=2)
        df.loc[df['Report Date'].isna() & df['Event Date'].notna()
               & df['Launch Date'].notna()
               & (df['Event Date'] - df['Launch Date'] <= dt.timedelta(days=3)),
               ['formal report date']] = df['Event Date'] - dt.timedelta(days=1)
        df.loc[df['Report Date'].isna() & df['Event Date'].notna()
               & df['Launch Date'].notna()
               & (df['Event Date'] - df['Launch Date'] <= dt.timedelta(days=2)),
               ['formal report date']] = df['Event Date']
        # 感谢信一般是launch data 晚于 event date, 特此列出。
        df.loc[df['Report Date'].isna() & df['Event Date'].notna()
               & df['Launch Date'].notna()
               & (df['Event Date'] - df['Launch Date'] <= dt.timedelta(days=0)),
               ['formal report date']] = df['Launch Date'] + dt.timedelta(
                   days=7)

        # 若report date是星期六，那么就要加两天，到星期一发报告
        df.loc[df['formal report date']
               .apply(lambda x: self.__turnWeekday(x) == 5),
               ['formal report date']] = df.loc[
                   df['formal report date']
                   .apply(lambda x: self.__turnWeekday(x) == 5),
                   ['formal report date']] + dt.timedelta(days=2)

        # 若report date是星期日，那么就要加一天，到星期一发报告
        df.loc[df['formal report date']
               .apply(lambda x: self.__turnWeekday(x) == 6),
               ['formal report date']] = df.loc[
                   df['formal report date']
                   .apply(lambda x: self.__turnWeekday(x) == 6),
                   ['formal report date']] + dt.timedelta(days=1)

        today = dt.date.today()

        # 处理参数
        def transfer_str(x):
            if isinstance(x, (int, float)):
                return str(x)
            else:
                return x

        def transfer_date(x):
            '''
            @description: 将参数转为dt.date
            @param {type} 
            @return: 
            '''
            if isinstance(x, str):
                x = x.lower()
            try:
                return parse(x).date()
            except ValueError:
                if x == "today":
                    return dt.date.today()
                elif x == "yesterday":
                    return dt.date.today() + dt.timedelta(-1)
                elif x == "tomorrow" or x == "tmr":
                    return dt.date.today() + dt.timedelta(1)
                

        args = list(map(transfer_str, args))
        args = list(map(transfer_date, args))

        df = df[df['formal report date'].apply(
            lambda x: isinstance(x, dt.date))]

        if len(args) == 0:
            report_df = df[df['formal report date'] == today]

        elif len(args) == 1:
            report_df = df[df['formal report date'] == args[0]]

        elif len(args) == 2:

            if args[1] > args[0]:
                report_df = df[(df['formal report date'] <= args[1])
                               & (df['formal report date'] >= args[0])]
            else:
                report_df = df[(df['formal report date'] <= args[0])
                               & (df['formal report date'] >= args[1])]

        else:
            raise ValueError('此方法只接收两个以下参数哦~')

        return report_df[['Campaign Name', 'Owner ', 'Launch Date', 'Weekday', 'Campaign ID', 'Event Date', 'Sent']]

        
    def check(self):
        '''
        @description: 
        @param {type} 
        @return: 所有过期的，且没有campaign id的条目 -> DataFrame
        '''
        df = self.getCleanDf()
        df = df[(df['Launch Date'] <= dt.date.today()) &
                (df['Launch Date'] >= self.getStartDate()) &
                (df['Campaign ID'].isnull().values == True)]  # 按时间筛选出今天以前的时间

        df = df.sort_values(by='Launch Date')  # 按顺序排列

        return df[['Campaign Name', 'Owner ', 'Launch Date', 'Campaign ID']]

    def waitWork(self):
        '''
        @description: 所有待定，临时取消等等的campaign
        @param {type} 
        @return: 
        '''
        '''
        表示待定的工作
        '''
        df = self.getVanillaDf()
        df = df[(df['Launch Date'].apply(lambda x: isinstance(x, str)))]

        return df[['Launch Date', 'Campaign Name', 'Owner ']]

    def communicationLimitHint(self):
        '''
        为第二天的campaign查看一周前的campaign
        '''
        # 先检验数据是否被清洗了

        df = self.getCleanDf()
        today = dt.date.today()

        the_date = today + dt.timedelta(days=-4)  # 计算4天前的日期
        the_date_for_friday = today + dt.timedelta(
            days=-2)  # 如果是周五，那实际上应该计算2天前的日期

        if today.weekday() == 4:  # 这个函数是从0算起，0代表星期一，4代表星期五
            df = df[(
                df['Launch Date'] == the_date_for_friday)]  # 筛选出4天前布置的campaign
        else:
            df = df[(df['Launch Date'] == the_date)]  # 筛选出6天前布置的campaign
        df = df.reset_index(drop=True)  # 重新索引

        try:
            df['Campaign ID'] = df['Campaign ID'].apply(lambda x: int(x))
        except ValueError:
            pass

        return df[['Campaign Name', 'Launch Date', 'Weekday', 'Campaign ID']]

    def findCol(self, colName) -> object:
        '''
        @description: 通过campaign id筛选出对应的attribute，若出现多campaign id的情况，一致取最后一个
        @param {str} 我们想要查找的列名 
        @return: 若我们只有一个参数，则返回一个str/int，若多个，则返回一个字典
        '''

        dic = {}
        df = self.getCleanDf()
        if len(self.getCampaignId()) == 1:
            return df[df['Campaign ID'] ==
                      self.getCampaignId()][colName].iloc[-1]

        for campaignId in self.getCampaignId():
            try:
                dic[campaignId] = df[df['Campaign ID'] ==
                                     campaignId][colName].iloc[-1]
            except IndexError:
                warnings.warn(
                    "RequestTracker中没有{}这个campaign id，请再验证，谢谢~".format(
                        campaignId), UserWarning)
                dic[campaignId] = None

        return dic

    def executionTime(self) -> object:
        return self.findCol('Launch Date')

    def name(self) -> object:
        return self.findCol('Campaign Name')

    def isHongKong(self, x):
        return "hong" in x.lower()

    def isTaiWan(self, x):
        return "tai" in x.lower()

    def isChina(self, x):
        return "china" in x.lower()

    def isWaveOne(self, campaignName: str):
        return not (('w2' in campaignName) or ('W2' in campaignName) or ('w3' in campaignName) or ('W3' in campaignName) or ('W4' in campaignName) or ('w4' in campaignName) or ('W5' in campaignName) or ('w5' in campaignName))

    def removeDuplicate(self, df: pd.DataFrame):
        return df[df['Campaign Name'].apply(lambda x: self.isWaveOne(x))]

    

    def timeRangeData(self, country: str, timeRange: tuple) -> pd.DataFrame:
        df = self.getCleanDf()
        if "china" in country.lower():
            df = df[df['MU'].apply(lambda x: self.isChina(x))]
        elif "hong" in country.lower():
            df = df[df['MU'].apply(lambda x: self.isHongKong(x))]
        elif "tai" in country.lower():
            df = df[df['MU'].apply(lambda x: self.isTaiWan(x))]

        df = df[(df['Launch Date'] > timeRange[0]) &
                (df['Launch Date'] < timeRange[1])]
        return df

    # overiew 是我们data命令的核心方法
    def overview(self, df: pd.DataFrame) -> dict:
        num = len(df)
        unique_df = self.removeDuplicate(df)
        uniqueNum = len(unique_df)
        touchPoints = df['Delivered'].sum()
        openRate = df['Opened'].sum() / df['Delivered'].sum()
        ctr = df['Click'].sum() / df['Delivered'].sum()
        uniqueCTR = df['Unique Click'].sum() / df['Delivered'].sum()
        clickToOpen = df['Unique Click'].sum() / df['Opened'].sum()
        openContact = df['Opened'].sum()
        webinar = len(unique_df[unique_df['Request Type'].apply(lambda x: 'webinar' in x.lower())])
        offline = len(unique_df[unique_df['Request Type'].apply(lambda x: 'offline' in x.lower())])
        edm = len(df[df['Request Type'].apply(lambda x: 'edm' in x.lower())])
        newsletter = len(df[df['Request Type'].apply(lambda x: 'newsletter' in x.lower() or 'digitalist' in x.lower())])
        nurture = len(df[df['Request Type'].apply(lambda x: 'nurture' in x.lower())])
        if num == 0:
            averTouch = 0
        else:
            averTouch = touchPoints / num

        events = len(unique_df[unique_df['Request Type'].apply(lambda x: 'invitation' in x.lower())])
        dic = {'Email Number': num,
               'Unique Number': uniqueNum,
               'Events': events,
               'Average touch': averTouch,
               'Touch Points': touchPoints,
               'Open Contacts': openContact,
               'webinar invitation': webinar,
               'offline invitation': offline,
               'EDM(assets)': edm,
               'nurture': nurture,
               'newsletter' : newsletter,
               'Open Rate': openRate,
               'Click to Open rate': clickToOpen,
               "CTR": ctr,
               "Unique CTR": uniqueCTR}

        return dic
    
    def owner(self):
        campaignId = self.getCampaignId()
        df = self.getCleanDf()
        return df[df['Campaign ID'] == campaignId]['Owner '].iloc[-1]
    
    def launchDate(self):
        """
        docstring
        """
        campaignId = self.getCampaignId()
        df = self.getCleanDf()
        return df[df['Campaign ID'] == campaignId]['Launch Date'].iloc[-1]



if __name__ == "__main__":
    a = Analytics(6414)
    df = a.removeDuplicate(a.getCleanDf())
   
    df = df[(df['Launch Date'] >= dt.date(2020,1,1)) & (df['Launch Date'] <= dt.date(2020,11,23))]
    df = df[df['MU'] == 'China']
    df = df[df['Request Type'] == 'Webinar Invitation']
    # print(df['Team'].value_counts())
    print(df[df['Team'] == 'Digital'])
    
    
