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

    @staticmethod
    def is_date(text: str):
        """
        :param text: the user's input, should be a str like yyyymmdd or yyyy-mm-dd
        :return: true if the input can be translated to a dt.date successfully
        """
        if text == '':
            return True
        try:
            dt.datetime.strptime(text, '%Y%m%d').date()
            return True
        except ValueError:
            try:
                dt.datetime.strptime(text, '%Y-%m-%d').date()
                return True
            except ValueError:
                return False

if __name__ == '__main__':
    a = DateHelper.is_date('2020-01-112')
    print(a)
