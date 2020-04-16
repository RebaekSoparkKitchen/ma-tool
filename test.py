import configparser as cp
import time
from Read_json import Read_json
import json
import pandas as pd
from Clean_df import EDM 
import datetime as dt
from pandas import Series

dic = {1:'x',2:'xs'}
a= 1
if a in dic.keys():
    dic.pop(a)


print(dic)
