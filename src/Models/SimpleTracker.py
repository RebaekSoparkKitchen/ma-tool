import datetime as dt
from src.Views.CalendarExcel import CalendarExcel
from src.Connector.MA import MA


class SimpleTracker:
    def __init__(self, days_diff=21, cols=None):
        if cols is None:
            cols = ['blast_date', 'campaign_name', 'event_date', 'owner_full_name', 'smc_campaign_id']
        self.days_diff = days_diff
        self.start_date = dt.datetime.now().date() + dt.timedelta(-int(days_diff))
        self.cols = cols

    def exist_data(self):
        sql = f"SELECT blast_date, campaign_name, wave, event_date, owner_full_name, " \
              f"smc_campaign_id " \
              f"from Request WHERE " \
              f"DATE(blast_date) > DATE('now', '-{self.days_diff} day', 'localtime') " \
              f"ORDER BY blast_date;"

        return MA().query(sql)

    def data(self):
        end_date = self.str2date(self.exist_data()[-1][0])
        dates_range = self.date_range(self.start_date, end_date)
        continuous_data = list(map(lambda x: self.date_placeholder(x), dates_range))
        exist_data = self.exist_data()
        exist_dates = list(map(lambda x: x[0], exist_data))
        for d in continuous_data:
            if d[0] not in exist_dates:
                exist_data.append(d)

        # sort
        new_data = sorted(exist_data, key=lambda date: self.str2date(date[0]))
        new_data = self.add_weekday(new_data)
        return new_data

    @staticmethod
    def date_range(start: dt.date, end: dt.date) -> list:

        dates = []
        diff = (end - start).days
        for i in range(diff):
            start += dt.timedelta(days=1)
            dates.append(start.strftime('%Y-%m-%d'))
        return dates

    def date_placeholder(self, date: str):
        dates = list([None for i in range(len(self.cols))])
        dates[0] = date
        return tuple(dates)

    @staticmethod
    def str2date(x):
        return dt.datetime.strptime(x, '%Y-%m-%d').date()

    def add_weekday(self, data):
        data = list(map(lambda x: list(x), data))
        mapper = ['一', '二', '三', '四', '五', '六', '日']
        for item in data:
            date = self.str2date(item[0])
            item.insert(1, '星期' + mapper[date.weekday()])
        return data

    def main(self, path: str):
        c = CalendarExcel(self.data())
        c.save(path)


if __name__ == '__main__':
    s = SimpleTracker()
    data = s.data()
    CalendarExcel(data).save(path=r'C:\Users\C5293427\Desktop\EDM\Simple.xlsx')
