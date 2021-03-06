import sys

sys.path.append("../..")
from src.Connector.MA import MA
from src.Models.Report.ClickPerformance import ClickPerformance
from src.Models.Report.BasicPerformance import BasicPerformance


class ReportData(object):
    __slots__ = ['campaign_name', 'blast_date', 'basic_performance', 'click_performance', 'wave']

    def __init__(self, smc_campaign_id):
        self.campaign_name = self.query_campaign_name(smc_campaign_id)
        self.blast_date = self.query_blast_date(smc_campaign_id)
        self.wave = self.query_wave(smc_campaign_id)
        self.click_performance = ClickPerformance.select(smc_campaign_id)
        self.basic_performance = BasicPerformance.select(smc_campaign_id)

    @staticmethod
    def query_campaign_id(smc_campaign_id: int or str) -> bool:
        count = MA().query(f"SELECT count(*) FROM BasicPerformance WHERE smc_campaign_id = '{smc_campaign_id}'")[0][0]
        return count != 0

    @staticmethod
    def query_blast_date(smc_campaign_id: int or str) -> list:
        return MA().query(f"SELECT blast_date FROM Request WHERE smc_campaign_id = '{smc_campaign_id}'")[0][0]

    @staticmethod
    def query_campaign_name(smc_campaign_id: int or str) -> list:
        return MA().query(f"SELECT campaign_name FROM Request WHERE smc_campaign_id = '{smc_campaign_id}'")[0][0]

    @staticmethod
    def query_wave(smc_campaign_id: int or str) -> list:
        return MA().query(f"SELECT wave FROM Request WHERE smc_campaign_id = '{smc_campaign_id}'")[0][0]

if __name__ == '__main__':
    print(ReportData.query_campaign_id(4227))
