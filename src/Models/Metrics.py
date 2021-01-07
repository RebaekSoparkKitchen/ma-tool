from src.Connector.MA import MA

class Metrics(object):
    def __init__(self, mu: str, time_range: tuple):
        self.mu = mu
        self.start = time_range[0]
        self.end = time_range[1]

    def data(self):
        sql =f"SELECT COUNT(*) AS email_number, " \
             f"COUNT(DISTINCT request_id) AS unique_email_number, " \
             f"(sum(opened) * 1.0)/sum(delivered) AS open_rate " \
             f"FROM request LEFT OUTER JOIN BasicPerformance USING (smc_campaign_id) " \
             f"WHERE MU = '{self.mu}' AND date(blast_date) BETWEEN date('{self.start}') AND date('{self.end}')"
        return MA().query(sql, as_dict=True)
if __name__ == '__main__':
    m = Metrics("Hong Kong", ('2020-01-01', '2020-12-31'))
    print(m.data())