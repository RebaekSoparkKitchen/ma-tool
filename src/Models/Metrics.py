import tablib
from src.Connector.MA import MA


class Metrics(object):
    def __init__(self, mu: str, time_range: tuple):
        self.mu = mu
        self.start = time_range[0]
        self.end = time_range[1]

    def general_number(self):
        if self.mu == 'GC':
            mu = 'IS NOT NULL'
        else:
            mu = f"= '{self.mu}'"
        statement = f"SELECT COUNT(1) AS 'Email Number', " \
                    f"COUNT(DISTINCT request_id) AS 'Unique Email Number', " \
                    f"SUM(delivered) AS 'Touch Points', " \
                    f"(SUM(delivered)/COUNT(1)) AS 'Average Touch Points', " \
                    f"(SUM(opened) * 1.0)/sum(delivered) AS 'Open Rate', " \
                    f"(SUM(unique_click) * 1.0)/sum(opened) AS 'Click to Open Rate', " \
                    f"(SUM(click) * 1.0)/sum(delivered) AS 'CTR', " \
                    f"(SUM(valid_click) * 1.0)/sum(delivered) AS 'Valid CTR', " \
                    f"(SUM(unique_click) * 1.0)/sum(delivered) AS 'Unique CTR' " \
                    f"FROM request LEFT OUTER JOIN BasicPerformance USING (smc_campaign_id) " \
                    f"WHERE MU {mu} AND date(blast_date) BETWEEN date('{self.start}') AND date('{self.end}')"

        return MA().query(statement, as_dict=True)[0]

    def event_number(self):
        if self.mu == 'GC':
            mu = 'IS NOT NULL'
        else:
            mu = f"= '{self.mu}'"
        sql = f"SELECT COUNT(DISTINCT request_id), request_type " \
              f"FROM request LEFT OUTER JOIN BasicPerformance USING (smc_campaign_id) " \
              f"WHERE MU {mu} AND date(blast_date) BETWEEN " \
              f"date('{self.start}') AND date('{self.end}') " \
              f"GROUP BY request_type"
        events = MA().query(sql)
        dic = {}
        for event in events:
            dic[event[1]] = event[0]
        return dic

    def total_number(self):
        dic = self.general_number()
        dic.update(self.event_number())
        return dic

    def tab_data(self):
        dic = self.total_number()
        data = tablib.Dataset()
        data.headers = list(dic)
        data.append(dic.values())
        return data

    def export(self, path, name):
        data = self.tab_data()
        with open(f"{path}/{name}.xlsx", 'wb') as f:
            f.write(data.export('xlsx'))


if __name__ == '__main__':
    m = Metrics("Taiwan", ('2020-01-01', '2020-12-31'))
    print(m.tab_data())
