from src.Connector.MA import MA


class TableData(object):
    def __init__(self, title, cols, content):
        self.title = title
        self.cols = cols
        self.content = content


def data_producer(title: str, cols: list, sql: str) -> TableData:
    return TableData(title=title, cols=cols, content=MA().query(sql))
