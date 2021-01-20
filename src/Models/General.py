from src.Connector.MA import MA

def if_exists(pk_id: str or int):
    sql = f"SELECT COUNT(1) FROM Request WHERE id = {pk_id}"
    result = MA().query(sql)
    return result[0][0] != 0

