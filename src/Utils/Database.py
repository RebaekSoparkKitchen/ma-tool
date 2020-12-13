from src.Control.MA import MA


def get_col_name(table_name: str):
    ma = MA()
    info = ma.sqlProcess("PRAGMA table_info(Request)")
    col_name = map(lambda x: x[1], info)
    return list(col_name)
