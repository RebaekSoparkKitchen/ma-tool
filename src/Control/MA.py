'''
@Description: 作为最高层级的类，让大家能方便读取配置文件
@Author: FlyingRedPig
@Date: 2020-08-03 11:47:04
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-19 11:19:58
@FilePath: \MA_tool\src\Control\MA.py
'''
import json
import sqlite3


class MA(object):
    def __init__(self):
        self.configPath = r'../../config/config.json'
        self.dataPath = r'../data/Request_Data.json'
        self.config = self.readConfig()
        self.dbAddress = self.config['data_location']['Database']
        self.username = self.config['username']

    def getConfigPath(self):
        return self.configPath

    def readData(self) -> dict:

        with open(self.dataPath, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
        return json_data

    def readConfig(self) -> dict:
        configPath = self.getConfigPath()
        with open(configPath, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
        return json_data

    def setConfig(self, attribute, data) -> None:
        configPath = self.getConfigPath()
        config = self.readConfig()
        config['username'] = data
        if config == {}:
            print("此更改将清空config文件， 请查看命令是否合理")
            return
        with open(configPath, "w") as f:
            json.dump(config, f)
        return

    def sqlProcess(self, *args) -> list:
        '''
        helper method -> 对于一切需要sql操作的方法
        '''
        assert len(args) > 0  # 您必须传一个命令进来，否则不要调用此方法
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
