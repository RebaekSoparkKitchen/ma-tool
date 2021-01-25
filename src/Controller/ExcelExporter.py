from src.Connector.MA import MA


class ExcelExporter(object):
    __slots__ = ['statement', 'file_name', 'path']

    def __init__(self, statement, path, file_name):
        self.statement = statement
        self.file_name = file_name
        self.path = path

    def export(self):
        rows = MA().query(self.statement, orm=True)
        with open(self.path + self.file_name, 'wb') as f:
            f.write(rows.export('xlsx'))

if __name__ == '__main__':
    e = ExcelExporter("select * from request left outer join BasicPerformance using (smc_campaign_id) where "
                      "campaign_name like '%rise%' --case-insensitive",
                      'C:/Users/C5293427/Desktop/EDM/analytics_data/', 'rise_with_sap.xlsx')
    e.export()
