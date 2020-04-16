import pandas as pd
from pandas import Series
from Clean_df import EDM
import datetime as dt

class Analytics(object):

    def __init__(self, campaign_id):
        path = r'C:\Users\C5293427\Desktop\MA\Request_Tracker.xlsx'
        e = EDM(path)
        df = e.clean_date()
        self.start_date = dt.date(2020,1,1)
        self.df = df[(df['Sent'].notna()) & (df['Launch Date'] > self.start_date)]

        self.campaign_id = int(campaign_id)
        df1 = df.set_index(["Campaign ID"], False) #方便我提取各种数据

        self.mu = df1.loc[campaign_id, 'MU']
        if type(self.mu) == pd.core.series.Series:  #以免出现多个campaign_id的情况
            self.mu = self.mu.iloc[-1]

        self.team = df1.loc[campaign_id, 'Team']
        if type(self.team) == pd.core.series.Series:
            self.team = self.team.iloc[-1]

    
    def get_df(self):
        return self.df

    def get_campaign_id(self):
        return self.campaign_id

    def get_mu(self):
        return self.mu

    def get_team(self):
        return self.team

    def total_open_rate(self):
        '''
        计算所有campaign的平均open rate
        '''
        df = self.get_df()
        return df['Opened'].sum()/df['Sent'].sum()

    def mu_open_rate(self):
        '''
        计算此mu的平均open rate
        '''
        mu = self.get_mu()
        df = self.get_df()

        df = df[df['MU'] == mu]

        return df['Opened'].sum()/df['Sent'].sum()

    def team_open_rate(self):
        '''
        计算此team的平均open rate
        '''

        team = self.get_team()
        df = self.get_df()

        df = df[df['Team'] == team]

        return df['Opened'].sum()/df['Sent'].sum()

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

    
