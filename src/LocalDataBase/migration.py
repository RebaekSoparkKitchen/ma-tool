"""
@Description: 当把数据迁移到sqlite时用到的脚本文件，不用做正式的操作中
@Author: FlyingRedPig
@Date: 2020-07-31 11:19:58
@LastEditors: FlyingRedPig
@LastEditTime: 2020-07-31 23:33:55
@FilePath: \EDM\edm\LocalDataBase\migration.py
"""
import sqlite3
import json
import datetime
import pandas as pd
from sqlalchemy import create_engine

# db_file = '../data/MarketingAutomation.db'

#与数据库建立联系
# conn = sqlite3.connect(db_file)

# #写sql语句
# sql = 'select * from ClickPerformance'

# #cur用来执行sql语句
# cur = conn.cursor()
# cur.execute(sql)
# print(cur.fetchall())
# conn.commit()
# conn.close()

def readConfig():
    """
    从config文件中读取tracker path
    """
    configPath = r'../config/config.json'
    with open(configPath,'r',encoding='utf8')as fp:
        json_data = json.load(fp)
    
    return json_data


def read():
    dataPath = r'../data/campaign_data.json'
    with open(dataPath,'r',encoding='utf8')as fp:
        json_data = json.load(fp)
    
    return json_data

def build(table):
    """
    预处理数据，使其能导入sqlite
    """
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = read()
    if table == 'click_performance':
        
        dic = {}
        
        for campaignId in data.keys():
            dic[campaignId]=data[campaignId][table]
        
        for campaignId in dic.keys():
            for row in dic[campaignId]:
                row['smc_campaign_id'] = campaignId
        
        dic2 = []
        for item in dic.values():
            for row in item:
                dic2.append(row)

        final = []
        for row in dic2:
            if_main_link = 1
            for i in readConfig()['other_link']:
                if row['Content Link Name'] in i:
                    if_main_link = 0
            new_row = (row['Clicks'], row['Content Link Name'], row['smc_campaign_id'],if_main_link, nowTime)
            final.append(new_row)
    
    elif table == 'basic_performance':
        dic= {}
        for campaignId in data.keys():
            dic[campaignId]=data[campaignId][table]
        
        for campaignId in dic.keys():
            dic[campaignId]['smc_campaign_id'] = campaignId

        
        final = dic

    return final

def to_basic_df():
    a = pull('basic_performance').values()
    df1 = pd.DataFrame(a)
    df2 = to_click_df()
    df1['valid_click'] = df1['smc_campaign_id'].apply(lambda x: df2[(df2['smc_campaign_id'] == str(x)) & (df2['if_main_link'] == 1)]['click_number'].sum())
    for column in df1.columns:
        if column == 'smc_campaign_id':
            continue
        else:
            df1[column] = df1[column].apply(lambda x: trans_int(x))
    return df1

def trans_int(x):
    try:
        return int(x)
    except ValueError:
        return x


def to_click_df():
    a = pull('click_performance')
    df = pd.DataFrame(a, columns=['click_number', 'link_name', 'smc_campaign_id', 'if_main_link', 'creation_time'])
    df['click_number'] = df['click_number'].apply(lambda x: trans_int(x))
    return df

def basic_add_more():
    df = to_basic_df()
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['bounce_rate'] = (df['Hard Bounces'] + df['Soft Bounces']) / df['Sent']
    df['open_rate'] = df['Opened'] / df['Delivered']
    df['unique_click_to_open_rate'] = df['Unique Click'] / df['Opened']
    df['valid_click_to_open_rate'] = df['valid_click'] / df['Opened']
    df['vanilla_click_to_open_rate'] = df['Click'] / df['Opened']
    df['ctr'] = df['Click'] / df['Delivered']
    df['unique_ctr'] = df['Unique Click'] / df['Delivered']

    df.rename(columns = {'Sent': 'sent', 'Hard Bounces': 'hard_bounces', 'Soft Bounces': 'soft_bounces', 'Delivered': 'delivered', 'Opened': 'opened', 'Click': 'click', 'Unique Click': 'unique_click'}, inplace = True)
    df['creation_time'] = nowTime
    df.fillna(0, inplace=True)
    return df
    

def pull(table):
    return build(table)


def push(data):
    db_file = '../data/MarketingAutomation.db'

    #与数据库建立联系
    conn = sqlite3.connect(db_file)

    #写sql语句
    #cur用来执行sql语句
    cur = conn.cursor()
    for item in data:
        if table == 'click_performance':
            cur.execute("INSERT INTO ClickPerformance (click_number, link_name, smc_campaign_id, if_main_link, creation_time) VALUES " + str(item))
        elif table == 'basic_performance':
            pass
    print(cur.fetchall())
    conn.commit()
    conn.close()
    return

def migrate(table):
    data = pull(table)
    push(data)
    return

df1 = to_basic_df()
df2 = to_click_df()

print(basic_add_more().columns)
print(basic_add_more())

engine = create_engine(r'sqlite:///C:\Users\C5293427\Desktop\research\EDM_project\EDM\data\MarketingAutomation.db')

basic_add_more().to_sql('BasicPerformance', engine)