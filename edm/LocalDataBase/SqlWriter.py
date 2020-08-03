'''
@Description:
data flow:
spider -> local_data(raw data) -> sql_computer(中间计算层) -> sql_writer(更完备的记录进入数据库)
                            -> report (只是分发一部分)
                            -> tracker (只是分发一部分)
从sql_computer接收basicData()和clickData()两个接口
既然local_data部分已经能保持正常运转，sql又想要更多更详细的数据，所以单拿出来
@Author: FlyingRedPig
@Date: 2020-07-31 17:56:28
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-03 11:58:18
@FilePath: \EDM\edm\LocalDataBase\SqlWriter.py
'''
import sys
sys.path.append("..")
import sqlite3
import pandas as pd
import json
from edm.LocalDataBase.SqlComputer import SqlComputer
from edm.Control.MA import MA


class SqlWriter(MA):

    def __init__(self, campaignId: int):

        config = self.readConfig()
        self.clickTable = 'ClickPerformance'
        self.basicTable = 'BasicPerformance'
        self.campaignIdAttribute = 'smc_campaign_id'
        self.dbAddress = config['location']['Database']
        self.campaignId = int(campaignId)
        data = SqlComputer(self.campaignId)
        self.basicData = data.getBasic()
        self.clickData = data.getClick()

    def readConfig(self) -> str:
        configPath = r'../config/config.json'
        with open(configPath,'r',encoding='utf8')as fp:
            json_data = json.load(fp)
        return json_data

    def __sqlProcess(self, *args) -> list:
        '''
        helper method -> 对于一切需要sql操作的方法
        '''
        assert len(args) > 0  #您必须传一个命令进来，否则不要调用此方法
        conn = sqlite3.connect(self.dbAddress)
        cur = conn.cursor()
        temp = []
        if len(args) == 1:
            sql = args[0]
            cur.execute(sql)
            temp = cur.fetchall()
        else:
            for sql in args:
                cur.execute(sql)
                temp.append(cur.fetchall())
        conn.commit()
        conn.close()
        return temp

    def check(self) -> bool:
        '''
        检查此campaign id是否已在数据库中
        已在数据库中 -> True
        不在数据库中 -> False
        '''
        sql1 = 'SELECT * FROM {} WHERE {}={}'.format(self.basicTable, self.campaignIdAttribute, self.campaignId)
        sql2 = 'SELECT * FROM {} WHERE {}={}'.format(self.clickTable, self.campaignIdAttribute, self.campaignId)
        result1, result2 = self.__sqlProcess(sql1, sql2)
        return (result1 != []) & (result2 != [])

    @staticmethod
    def __insert(table: str, attribute: tuple, data: tuple):
        return "INSERT INTO {} {} VALUES {}".format(table, str(attribute), str(data)) 
    
    def insertIntoBasic(self) -> None:
        '''
        向BasicPerformance表插入此campaign id的数据
        '''
        basic = self.basicData

        attribute = ('smc_campaign_id','sent','hard_bounces','soft_bounces','delivered', 'opened', 'click', 'unique_click', 'valid_click', 'bounce_rate', 'open_rate', 'unique_click_to_open_rate', 'valid_click_to_open_rate', 'vanilla_click_to_open_rate', 'ctr', 'unique_ctr', 'creation_time')

        data = (basic['smc_campaign_id'], basic['Sent'], basic['Hard Bounces'], basic['Soft Bounces'], basic['Delivered'], basic['Opened'], basic['Click'], basic['Unique Click'], basic['valid_click'], basic['bounce_rate'], basic['open_rate'], basic['unique_click_to_open_rate'], basic['valid_click_to_open_rate'], basic['vanilla_click_to_open_rate'], basic['ctr'], basic['unique_ctr'], basic['creation_time'])

        sql = SqlWriter.__insert(self.basicTable, attribute, data)
        self.__sqlProcess(sql)
        return 

    def insertIntoClick(self) -> None:
        '''
        向ClickPerformance表插入此campaign id的数据
        '''
        click = self.clickData
        attribute = ('smc_campaign_id', 'link_name', 'click_number', 'link_alias', 'if_main_link', 'creation_time')
        sqlList = []
        for item in click:
            data = (item['smc_campaign_id'], item['Content Link Name'], item['Clicks'], item['Link Alias'], item['if_main_click'], item['creation_time'])
            sql = SqlWriter.__insert(self.clickTable, attribute, data)
            sqlList.append(sql)
        sqlTuple = tuple(sqlList)
        self.__sqlProcess(*sqlTuple)
        return 
    
    def delete(self, table: str) -> list:
        '''
        删除此数据库下所有带有此campaign id的数据
        '''
        assert table in [self.basicTable, self.clickTable] 
        sql = "DELETE from {} where smc_campaign_id={};".format(table, str(self.campaignId))
        self.__sqlProcess(sql)
        return 
             

    def push(self, overwrite: bool) -> None:
        assert type(overwrite) == bool
        #在非覆盖，数据库中有值的情况下才直接return，其他情况都是要与数据库交互的
        if not overwrite:
            if self.check():
                return 
        if self.check():
            self.delete(self.clickTable)
            self.delete(self.basicTable)
        self.insertIntoClick()
        self.insertIntoBasic()
        return 




        

