import pandas as pd
import datetime as dt
import warnings
from dateutil.parser import parse
import numpy as np
import openpyxl
from openpyxl.styles import Font, colors, Alignment, Border, Side, PatternFill
from IPython.display import display, HTML
from time import time


class EDM(object):
    '''
    这个类的作用是提取出干净的 dataframe，供展示、操作类调用
    '''

    def __init__(self, path):

        # 这个dataframe是读取的excel中的Tracker页面
        self.dataframe = pd.read_excel(path, encoding = 'utf-8')
        self.dataframe1 = self.dataframe
        self.wait_work = self.dataframe

    def get_dataframe(self):

        return self.dataframe

    def get_dataframe1(self):
        '''
        :return:
        '''
        return self.dataframe1

    def trans_date(self, x):
        try:
            return x.date()
        except AttributeError:
            return x

    def clean_date(self):
        '''
        清理空值和invalid value
        将datetime格式 --> date格式

        '''

        df = self.get_dataframe()  # 获取数据
        # 给列改名字
        self.wait_work = df[df['Launch Date'].apply(lambda x: isinstance(x, str))]

        for col in ['Launch Date', 'Event Date', 'Report Date']:
            df[col] = df[col].apply(lambda x: self.trans_date(x))   #把涉及时间的列转换为date类型
             
        df = df[df['Launch Date'].apply(lambda x: isinstance(x, dt.date))]

        df['weekday'] = df['Launch Date'].apply(lambda x: self.turn_weekday(x))

        return df

    def turn_weekday(self, x):
        '''
        help function
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
            return np.nan



if __name__ == '__main__':
    t_path = r'C:\Users\C5293427\Desktop\MA\Request_Tracker.xlsx'
    s_path = r'C:\Users\C5293427\Desktop\MA\Simple_Tracker_V3.xlsx'
    EDM_file = EDM(t_path)
    df = EDM_file.clean_date()
    print(df['Event Date'][df['Event Date'].apply(lambda x: isinstance(x, dt.date))].max())
    #print(df['Event Date'].max())


   