import datetime as dt


class DateHelper(object):
    @staticmethod
    def str_to_date(str_p: str) -> dt.date:
        try:
            date = dt.datetime.strptime(str_p, '%Y%m%d').date()
        except ValueError:
            date = dt.datetime.strptime(str_p, '%Y-%m-%d').date()
        return date

    @staticmethod
    def date_to_str(date_p: dt.date or dt.datetime) -> str:
        str_p = dt.datetime.strftime(date_p, '%Y-%m-%d')
        return str_p


if __name__ == '__main__':
    a = DateHelper.str_to_date('20200112')
    print(a)
