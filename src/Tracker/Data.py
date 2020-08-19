'''
@Description: extract some data for qbr
@Author: FlyingRedPig
@Date: 2020-07-06 16:26:03
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-19 10:48:15
@FilePath: \MA_tool\src\Tracker\Data.py
'''

from src.Tracker.Analytics import Analytics 
from src.Control.MA import MA
import pandas as pd
from dateutil.parser import parse
import sys
sys.path.append("..")


class DataExtractor(MA):

    def __init__(self):
        super().__init__()

    @staticmethod
    def add_row(df: pd.DataFrame, dic: dict) -> pd.DataFrame:
        data = pd.DataFrame(dic)
        df = df.append(data, ignore_index=True)
        return df

    @staticmethod
    def str2date(string: str):
        return parse(str(string)).date()

    
    def save(self, country, time1, time2):
        
        path = self.readConfig()['file_location']['Analytics']
        time1_date = DataExtractor.str2date(time1)
        time2_date = DataExtractor.str2date(time2)
        a = Analytics()
        df = a.timeRangeData(country, (time1_date, time2_date))
        dic = a.overview(df)
        df = pd.DataFrame(dic, index=[0])
        df.to_excel(path + country+"_" +
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
