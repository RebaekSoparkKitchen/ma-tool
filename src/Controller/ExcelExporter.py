from src.Connector.MA import MA


class ExcelExporter(object):
    __slots__ = ['statement', 'path']

    def __init__(self, statement, path):
        self.statement = statement
        self.path = path

    def export(self):
        rows = MA().query(self.statement, orm=True)
        with open(self.path, 'wb') as f:
            f.write(rows.export('xlsx'))

if __name__ == '__main__':
    e = ExcelExporter("select * from request left outer join BasicPerformance using (smc_campaign_id) where "
                      "(team == 'HK Marketing' or team == 'CX Demand Generation Hong Kong') and date(blast_date) >= date('2021-01-01') "
                      "--case-insensitive ",
                      'C:/Users/C5293427/Desktop/EDM/analytics_data/HK_2021.xlsx')
    # e = ExcelExporter("select id, blast_date from request where "
    #                   "date(blast_date) between date('2020-01-01') and date('2020-12-31') ",
    #                   'C:/Users/C5293427/Desktop/EDM/analytics_data/', 'rise_with_sap.xlsx')
    e.export()
