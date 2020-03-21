import configparser as cp
import time
from Read_json import Read_json
import json
import pandas as pd
from Clean_df import EDM 
import datetime as dt

config = cp.ConfigParser()
config.read('config.ini', 'UTF-8')

t_path = r'C:\Users\C5293427\Desktop\MA\Request_Tracker.xlsx'
s_path = r'C:\Users\C5293427\Desktop\MA\Simple_Tracker_V3.xlsx'
EDM_file = EDM(t_path)
df = EDM_file.clean_date()
df['Event Date'].dropna(inplace=True)
print(df['Event Date'].max())

