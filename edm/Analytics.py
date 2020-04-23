'''
@Description: Analytics是非常重要的类，它是继承于RequestTracker，为report以及界面展示提供服务。
@Author: FlyingRedPig
@Date: 2020-04-07 12:22:06
@LastEditors: FlyingRedPig
@LastEditTime: 2020-04-23 17:40:00
@FilePath: \EDM\edm\Analytics.py
'''

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from RequestTracker import *
import datetime as dt
from dateutil.parser import parse


class Analytics(Request_Tracker):

    def __init__(self, *args):

        super(Analytics, self).__init__(*args)
        currentYear = dt.now().year
        df = self.getCleanDf()
        self.startDate = dt.date(currentYear, 1, 1)
        self.ytdData = df[df['Launch Date'] > self.startDate]

    def setStartDate(self, startDate: dt.date):
        self.startDate = startDate
        return

    def getStartDate(self):
        return self.startDate

    def getYtdData(self):
        return self.ytdData

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

    def report(self, *args="today"):
        '''
        @description: report方法给出我们需要今天report的dataframe
        @param {df:DataFrame, *args:str} *args代表
        @return: DataFrame
        '''
        args = *args
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
        df.loc[
            df['formal report date'].apply(lambda x: self.turn_weekday(x) == 5),
            ['formal report date']] = df.loc[
                df['formal report date']
                .apply(lambda x: self.turn_weekday(x) == 5),
                ['formal report date']] + dt.timedelta(days=2)

        #若report date是星期日，那么就要加一天，到星期一发报告
        df.loc[
            df['formal report date'].apply(lambda x: self.turn_weekday(x) == 6),
            ['formal report date']] = df.loc[
                df['formal report date']
                .apply(lambda x: self.turn_weekday(x) == 6),
                ['formal report date']] + dt.timedelta(days=1)

        today = dt.date.today()

        #处理参数
        def transfer_str(x):
            if isinstance(x,(int, float)):
                return str(x)
            else:
                return x

        def transfer_date(x):
            return parse(x).date()

        args = map(transfer_str(),args)
        args = map(transfer_date(),args)
        
        if len(args) == 0:
            date = today
            report_df = df[df['formal report date'] == date]

        elif len(args) == 1:
            if args[0] == 'today':
                date = today
            report_df = df[df['formal report date'] == date]
    
        elif len(args) == 2:
            if args[0] == 'today':
                dateRange = (today, args[1])
            elif args[1] == 'today':
                dateRange = (args[0], today)
            
            if dateRange[1] > dateRange[0]:
                report_df = df[(df['formal report date'] <= dateRange[1]) & (df['formal report date'] >= dateRange[0])]
            else:
                report_df = df[(df['formal report date'] <= dateRange[0]) & (df['formal report date'] >= dateRange[1])]
        
        else:
            raise TypeError('此方法只接收两个以下参数哦~')

        return report_df[[
            'Campaign Name', 'Launch Date', 'weekday', 'Campaign ID',
            'Event Date', 'formal report date', 'Report Date'
        ]]

    def total_open_rate(self):
        '''
        计算所有campaign的平均open rate
        '''
        df = self.get_df()
        return df['Opened'].sum() / df['Sent'].sum()

    def mu_open_rate(self):
        '''
        计算此mu的平均open rate
        '''
        mu = self.get_mu()
        df = self.get_df()

        df = df[df['MU'] == mu]

        return df['Opened'].sum() / df['Sent'].sum()

    def team_open_rate(self):
        '''
        计算此team的平均open rate
        '''

        team = self.get_team()
        df = self.get_df()

        df = df[df['Team'] == team]

        return df['Opened'].sum() / df['Sent'].sum()

    def data_package(self):
        '''
        制作一个列表，通过Operation.Report的api传进去
        '''

        package = [(self.total_open_rate(), 'Overall average open rate'),
                   (self.mu_open_rate(), 'Your MU average open rate'),
                   (self.team_open_rate(), 'Your team average open rate')]

        return package


if __name__ == "__main__":
    a = Analytics(5756)
    print(a.mu)
    print(a.team)
