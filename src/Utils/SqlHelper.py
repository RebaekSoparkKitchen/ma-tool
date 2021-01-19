from typing import Iterable
import datetime as dt

def insert(table: str, cols: Iterable, values: Iterable) -> str:
    cols = tuple(cols)
    values = tuple(values)
    sql = "INSERT INTO {} {} VALUES {}".format(table, str(cols), str(values))
    return sql


def update(table: str, cols: Iterable[str] or str, values: Iterable[str] or str, pk_id: int) -> str:
    if not (isinstance(cols, list) or isinstance(cols, tuple)):
        cols = [cols]
        values = [values]
    statement = []
    for i in range(len(cols)):
        statement.append(f"{cols[i]}='{values[i]}'")
    statement = ','.join(statement)
    now = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S')
    sql = f"UPDATE {table} SET {statement}, last_modified_time = '{now}' WHERE id = {pk_id}"
    return sql

if __name__ == '__main__':
    a = update('request', 'blast_date', '20201012', 123)
    print(a)
    print(isinstance(1, Iterable))
