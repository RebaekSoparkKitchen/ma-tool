'''
@Description: extract some data for qbr
@Author: FlyingRedPig
@Date: 2020-07-06 16:26:03
@LastEditors: FlyingRedPig
@LastEditTime: 2020-07-13 13:52:56
@FilePath: \EDM_project\EDM\bin\data.py
'''
import datetime as dt
import pandas as pd
from tabulate import tabulate
from dateutil.parser import parse
from edm.Transfer.gui import DataTransfer
from edm.Report.ReportExcel import ReportExcel
from edm.LocalDataBase.LocalData import LocalData
from edm.Spider.ClickPerformance import ClickPerformance
from edm.Spider.BasicPerformance import BasicPerformance
from edm.Tracker.WriteTracker import WriteTracker
from edm.Tracker.SimpleTracker import SimpleTracker
from edm.Tracker.Analytics import Analytics
import sys
sys.path.append("..")
sys.path.append("../edm/LocalDataBase/")


class DataExtractor(object):

    @staticmethod
    def add_row(df: pd.DataFrame, dic: dict) -> pd.DataFrame:
        data = pd.DataFrame(dic)
        df = df.append(data, ignore_index=True)
        return df

    @staticmethod
    def str2date(string: str):
        return parse(str(string)).date()

    @staticmethod
    def save(country, time1, time2):
        time1_date = DataExtractor.str2date(time1)
        time2_date = DataExtractor.str2date(time2)
        a = Analytics()
        df = a.timeRangeData(country, (time1_date, time2_date))
        dic = a.overview(df)
        df = pd.DataFrame(dic, index=[0])
        df.to_excel("../../analytics_data/" + country+"_" +
                    time1+"_" + time2+".xlsx", index=False)
        return


if __name__ == "__main__":

    a = Analytics()
    time1 = DataExtractor.str2date("20200401")
    time2 = DataExtractor.str2date("20200630")

    hk_q2 = a.timeRangeData("hongkong", (time1, time2))
    #tw_q2 = a.timeRangeData("taiwan", (time1, time2))
    b = a.overview(hk_q2)
    df = pd.DataFrame(b, index=[0])

    DataExtractor.save("Hongkong", "20200401", "20200630")
