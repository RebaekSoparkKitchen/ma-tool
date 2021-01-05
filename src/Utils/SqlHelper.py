from typing import Iterator
from src.Connector.MA import MA


def insert(table: str, cols: Iterator[str], values: Iterator[str]) -> str:
    cols = tuple(cols)
    values = tuple(values)
    sql = "INSERT INTO {} {} VALUES {}".format(table, str(cols), str(values))
    return sql

