"""
@Description: 作为最高层级的类，让大家能方便读取配置文件
@Author: FlyingRedPig
@Date: 2020-08-03 11:47:04
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-19 11:19:58
@FilePath: \MA_tool\src\Control\MA.py
"""
import json
import sqlite3
from collections import Iterable
from typing import Iterator


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

    def query(self, statement: str or Iterator, as_dict=False, orm=False):
        """
        sql 操作的简单封装
        :param orm: if using record to query
        :param statement: could be a single statement or a list of statement
        :param as_dict: if output a dictionary (key : col_names, value: data)
        :return:
        """
        if orm:
            import records
            db = records.Database(f'sqlite:///{self.db_address}')
            conn = db.get_connection()
            rows = conn.query(statement)
            return rows

        conn = sqlite3.connect(self.db_address)

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        if as_dict:
            conn.row_factory = dict_factory

        cur = conn.cursor()
        if isinstance(statement, str):
            cur.execute(statement)
        elif isinstance(statement, Iterable):
            for item in statement:
                cur.execute(item)
        result = cur.fetchall()
        conn.commit()
        conn.close()
        return result
