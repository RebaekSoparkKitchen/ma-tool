import datetime as dt
from dateutil.parser import parse
from Clean_df import EDM
import pandas as pd
import numpy as np
import time


class Display(object):

    def __init__(self, df):
        '''
        :param df: 指经过clean的dataframe对象
        '''
        self.dataframe = df

    def get_dataframe(self):
        return self.dataframe

    def future_work(self):
        '''
        输出： 我还未完成的工作
        '''
        df = self.get_dataframe()  #读取数据
        
        today = dt.date.today()  #获取此时此刻的时间
        df = df[(df['Launch Date']>today)]  #按时间筛选出今天以后的时间
        df = df.sort_values(by='Launch Date')  #按顺序排列
        df = df.reset_index(drop = True)  #重新索引
        
        df1 = df[['Campaign Name','Owner ','Launch Date','weekday']]
        
        if df.empty == True:
            return "There's no campaign in the future"
        
        return df1


    def select_date(self, date_str):

        if type(date_str) == int:
            date_str = str(date_str)
        df = self.get_dataframe()
        
        date = parse(date_str).date()
        df = df[df['Launch Date'] == date]  # 按时间筛选出今天以后的时间
        df = df.reset_index(drop=True)  # 重新索引

        if df.empty == True:
            return "There's no campaign on" + " " + date_str + '.'

        return df[['Campaign Name', 'Launch Date', 'weekday']]
    
    def turn_weekday(self, x):
        '''
        help function
        '''
        try:
            return x.weekday()
        except AttributeError:
            return np.nan

    def report(self):
        '''
        return 我该report的东西
        '''

        df = self.get_dataframe()
        today = dt.date.today()

        #必须让类型统一，把launch Date中的字符串删掉
        df.loc[df['Launch Date'].apply(lambda x: isinstance(x, str)), 'Launch Date'] = np.nan

        df['formal report date'] = df['Report Date']

        df.loc[df['Report Date'].isna() & df['Event Date'].isna() & df['Launch Date'].isna(), ['formal report date']] = np.nan
        df.loc[df['Report Date'].isna() & df['Event Date'].isna() & df['Launch Date'].notna(), ['formal report date']] = df['Launch Date'] + dt.timedelta(days=7)
        df.loc[df['Report Date'].isna() & df['Event Date'].notna() & df['Launch Date'].isna(), ['formal report date']] = np.nan
        df.loc[df['Report Date'].isna() & df['Event Date'].notna() & df['Launch Date'].notna() 
               & (df['Event Date'] - df['Launch Date'] > dt.timedelta(days=7)), ['formal report date']] = df['Launch Date'] + dt.timedelta(days=7)
        df.loc[df['Report Date'].isna() & df['Event Date'].notna() & df['Launch Date'].notna() 
               & (df['Event Date'] - df['Launch Date'] <= dt.timedelta(days=7)), ['formal report date']] = df['Event Date'] - dt.timedelta(days=2)
        df.loc[df['Report Date'].isna() & df['Event Date'].notna() & df['Launch Date'].notna() 
               & (df['Event Date'] - df['Launch Date'] <= dt.timedelta(days=3)), ['formal report date']] = df['Event Date'] - dt.timedelta(days=1)
        df.loc[df['Report Date'].isna() & df['Event Date'].notna() & df['Launch Date'].notna() 
               & (df['Event Date'] - df['Launch Date'] <= dt.timedelta(days=2)), ['formal report date']] = df['Event Date']
        
        #若report date是星期六，那么就要加两天，到星期一发报告
        df.loc[df['formal report date'].apply(lambda x: self.turn_weekday(x)==5), ['formal report date']] = df.loc[df['formal report date'].apply(lambda x: self.turn_weekday(x)==5), ['formal report date']]+ dt.timedelta(days=2)
        
        #若report date是星期日，那么就要加一天，到星期一发报告
        df.loc[df['formal report date'].apply(lambda x: self.turn_weekday(x)==6), ['formal report date']] = df.loc[df['formal report date'].apply(lambda x: self.turn_weekday(x)==6), ['formal report date']]+ dt.timedelta(days=1)
        
        report_df = df[df['formal report date'] == today]

        return report_df[['Campaign Name', 'Launch Date', 'weekday', 'Campaign ID', 'Event Date', 'formal report date', 'Report Date']]


    def check(self):
        '''
        input: self
        output: 所有过期的，没有campaign id的条目
        '''

        df = self.get_dataframe()
        today = dt.date.today()

        df = df[df['Launch Date'] <= today]  # 按时间筛选出今天以后的时间

        df = df.sort_values(by='Launch Date')  # 按顺序排列
        df = df[df['Campaign ID'].isnull().values == True]
        df = df.reset_index(drop=True)

        return df[['Campaign Name', 'Owner ', 'Launch Date', 'Campaign ID']]


    def wait_work(self):
        '''
        表示待定的工作
        '''

        df = self.get_dataframe()
    

        df.rename(columns={'Launch Date\n(Actual Date)': 'Launch Date'}, inplace=True)  # change name
        # 增加weekday

        df = df[(df['Launch Date'].apply(lambda x:isinstance(x,str)))]

        return df[['Campaign Name', 'Owner ', 'Launch Date']]


    def communication_limit_hint(self):
        '''
        为第二天的campaign查看一周前的campaign
        '''
        # 先检验数据是否被清洗了

        df = self.get_dataframe()
       
        today = dt.date.today()

        the_date = today + dt.timedelta(days=-6)  # 计算6天前的日期
        the_date_for_friday = today + dt.timedelta(days=-4)  # 如果是周五，那实际上应该计算4天前的日期

        if today.weekday() == 4:
            df = df[(df['Launch Date'] == the_date_for_friday)]  # 筛选出4天前布置的campaign
            df = df.reset_index(drop=True)  # 重新索引
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

if __name__ == '__main__':
    t_path = r'C:\Users\C5293427\Desktop\MA\Request_Tracker20190523.xlsx'
    s_path = r'C:\Users\C5293427\Desktop\MA\Simple_Tracker_V3.xlsx'
    EDM_file = EDM(t_path)
    c = EDM_file.clean_date()

    d = Display(c)
    start = time.time()
    df = d.report()
    print(df)
    end = time.time()
    df.to_excel(r'C:\Users\C5293427\Desktop\MA\rrrrr.xlsx',index=False)
    print(end-start)


    

 


