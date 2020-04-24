'''
@Description: Analytics是非常重要的类，它是继承于RequestTracker，为report以及界面展示提供服务。
@Author: FlyingRedPig
@Date: 2020-04-07 12:22:06
@LastEditors: FlyingRedPig
@LastEditTime: 2020-04-24 15:48:04
@FilePath: \EDM\edm\Analytics.py
'''

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from RequestTracker import *
import datetime as dt
from dateutil.parser import parse, _parser


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

        today = dt.date.today()  #获取此时此刻的时间
        df = df[(df['Launch Date'] > today)]  #按时间筛选出今天以后的时间
        df = df.sort_values(by='Launch Date')  #按顺序排列

        if df.empty == True:
            return "There's no campaign in the future"
        return df[[
            'Campaign Name', 'Owner ', 'Launch Date', 'weekday', 'Report Date'
        ]]

    def report(self, *args):
        '''
        @description: report方法给出我们需要今天report的dataframe
        @param {df:DataFrame, *args:str} *args代表
        @return: DataFrame
        '''

        df = self.getCleanDf()

        #必须让类型统一，把launch Date中的字符串删掉
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

        #若report date是星期六，那么就要加两天，到星期一发报告
        df.loc[df['formal report date']
               .apply(lambda x: self.__turnWeekday(x) == 5),
               ['formal report date']] = df.loc[
                   df['formal report date']
                   .apply(lambda x: self.__turnWeekday(x) == 5),
                   ['formal report date']] + dt.timedelta(days=2)

        #若report date是星期日，那么就要加一天，到星期一发报告
        df.loc[df['formal report date']
               .apply(lambda x: self.__turnWeekday(x) == 6),
               ['formal report date']] = df.loc[
                   df['formal report date']
                   .apply(lambda x: self.__turnWeekday(x) == 6),
                   ['formal report date']] + dt.timedelta(days=1)

        today = dt.date.today()

        #处理参数
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
            except _parser.ParserError:
                if x == "today":
                    return dt.date.today()
                elif x == "yesterday":
                    return dt.date.today() + dt.timedelta(-1)
                elif x == "tomorrow" or x == "tmr":
                    return dt.date.today() + dt.timedelta(1)
                else:
                    raise _parser.ParserError("请输入正确格式的日期字样~")

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
            raise TypeError('此方法只接收两个以下参数哦~')

        return report_df[[
            'Campaign Name', 'Launch Date', 'weekday', 'Campaign ID',
            'Event Date', 'formal report date', 'Report Date'
        ]]

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

        return df[['Campaign Name', 'Owner ', 'Launch Date']]

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

        if today.weekday() == 4:  #这个函数是从0算起，0代表星期一，4代表星期五
            df = df[(
                df['Launch Date'] == the_date_for_friday)]  # 筛选出4天前布置的campaign
        else:
            df = df[(df['Launch Date'] == the_date)]  # 筛选出6天前布置的campaign
        df = df.reset_index(drop=True)  # 重新索引

        try:
            df['Campaign ID'] = df['Campaign ID'].apply(lambda x: int(x))
        except ValueError:
            pass

        if df.empty == True:
            return "There's no concern for communication limit."

        return df[['Campaign Name', 'Launch Date', 'weekday', 'Campaign ID']]

    def total_open_rate(self):
        '''
        计算所有campaign的平均open rate
        '''
        df = self.get_df()
        return df['Opened'].sum() / df['Sent'].sum()


if __name__ == "__main__":
    a = Analytics(1234, 2312, 3212)
    print(a.futureWork())
