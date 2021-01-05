import sys

sys.path.append("../..")
from src.Connector.MA import MA
from src.Models.Report.ClickPerformance import ClickPerformance
from src.Models.Report.BasicPerformance import BasicPerformance


class ReportData(object):
    __slots__ = ['blast_date', 'basic_performance', 'click_performance']

    def __init__(self, blast_date, basic_performance, click_performance):
        self.blast_date = blast_date
        self.basic_performance = basic_performance
        self.click_performance = click_performance

    @staticmethod
    def select(smc_campaign_id):
        blast_date = MA().query(f"select blast_date from request where smc_campaign_id = {smc_campaign_id}")
        basic = MA().query(f"select {','.join(BasicPerformance.__slots__)} from BasicPerformance where "
                                 f"smc_campaign_id = '{smc_campaign_id}'", as_dict=True)
        clicks = MA().query(f"select {','.join(ClickPerformance.__slots__)} from ClickPerformance where "
                                  f"smc_campaign_id = "
                                  f"'{smc_campaign_id}'", as_dict=True)
        click_collection = list(map(lambda x: ClickPerformance(x), clicks))

        data = ReportData(blast_date=blast_date, basic_performance=BasicPerformance(basic[-1]),
                          click_performance=click_collection)
        return data




if __name__ == '__main__':
    import time
    t1 = time.time()
    a = ReportData.select(4227)
    t2 = time.time()
    print(t2 - t1)
    print(a.basic_performance.hard_bounces)

