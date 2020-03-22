import configparser as cp
import time
from Read_json import Read_json
import json
import pandas as pd
from Clean_df import EDM 
import datetime as dt

with open("config.json", "r", encoding='utf-8') as f:
    config = json.loads(f.read())    # load的传入参数为字符串类型
print(config)

