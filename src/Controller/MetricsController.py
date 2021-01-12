from src.Models.Metrics import Metrics
from src.Connector.MA import MA
import datetime as dt


class MetricsController(object):
    def __init__(self, mu, date1, date2):
        """
        所有参数都是用户手写输入的
        :param mu: 用户手写输入的国家名称
        :param date1:
        :param date2:
        """
        # 约束：日期1 必须小于 日期2
        assert dt.datetime.strptime(str(date1), '%Y%m%d') <= dt.datetime.strptime(str(date2), '%Y%m%d')
        self.origin_date1 = str(date1)
        self.origin_date2 = str(date2)
        self.mu = self.mu_mapper(mu)
        self.date1 = self.date_mapper(str(date1))
        self.date2 = self.date_mapper(str(date2))

    @staticmethod
    def mu_mapper(mu: str) -> str:
        """
        hk -> Hong Kong
        cn -> China
        tw -> Taiwan
        :param mu: 用户手写的名称
        :return:
        """
        # 对于命令的约束
        assert mu.lower() in ['hk', 'hongkong', 'tw', 'taiwan', 'cn', 'china', 'gc']

        if mu.lower() in ['hk' or 'hongkong']:
            return 'Hong Kong'
        if mu.lower() in ['tw' or 'taiwan']:
            return 'Taiwan'
        if mu.lower() in ['cn' or 'China']:
            return 'China'
        if mu.lower() in ['gc']:
            return 'GC'

        raise Exception(ValueError, 'name should be in [cn, tw, hk]')

    @staticmethod
    def date_mapper(date: str) -> str:
        """
        20201223 -> 2020-12-23
        :param date:用户手写输入的日期
        :return:
        """
        date = dt.datetime.strptime(date, '%Y%m%d')
        date = date.strftime('%Y-%m-%d')
        return date

    def file_name(self):
        mu = self.mu.replace(' ', '').lower()
        return f"{mu}_{self.origin_date1}_{self.origin_date2}"

    def export(self):
        m = Metrics(self.mu, (self.date1, self.date2))
        m.export(MA().read_config()['file_location']['Analytics'], self.file_name())


if __name__ == '__main__':
    m = MetricsController('hk', 20200101, 20201221)
    a = MetricsController.mu_mapper('tw')
    print(a)
