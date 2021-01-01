from src.Connector.MA import MA
import datetime as dt


class Uploader(object):
    def __init__(self, pk_id: int, table: str, col: str, data: str):
        """
        :param pk_id: primary key id
        :param table: table name
        :param col: col name
        :param data: the data you want to update in certain col for certain primary key
        """
        self.pk_id = pk_id
        self.col = col
        self.data = data
        self.table = table

    def upload(self):
        now = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S')
        if not self.data:
            return
        sql = f"UPDATE {self.table} " \
              f"SET {self.col} = {self.data}, last_modified_time = '{now}' " \
              f"WHERE id = {self.pk_id};"
        MA().sql_process(sql)
