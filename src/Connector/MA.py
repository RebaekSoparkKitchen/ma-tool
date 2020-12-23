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
        self.config_path = r'../../config/config.json'
        self.config = self.read_config()
        self.db_address = self.config['data_location']['Database']
        self.username = self.config['username']

    def read_data(self, data_name='Request_Data') -> dict:
        data_path = f'../data/{data_name}.json'
        with open(data_path, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
        return json_data

    def read_config(self) -> dict:
        with open(self.config_path, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
        return json_data

    def set_config(self, attribute, data) -> None:
        config = self.read_config()
        config['username'] = data
        if config == {}:
            print("此更改将清空config文件， 请查看命令是否合理")
            return
        with open(self.config_path, "w") as f:
            json.dump(config, f)
        return

    def sql_process(self, *args) -> list:
        """
        helper method -> 对于一切需要sql操作的方法
        :param args:
        :return:
        """

        assert len(args) > 0  # 您必须传一个命令进来，否则不要调用此方法
        conn = sqlite3.connect(self.db_address)
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
