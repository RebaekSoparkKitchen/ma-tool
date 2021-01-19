
import datetime as dt


def report_date_gen(blast: dt.date, event: dt.date) -> dt.date:
    if not blast:
        report_date = None
    elif not event:
        report_date = blast + dt.timedelta(days=7)
    else:
        if (event - blast > dt.timedelta(days=7)) or (event - blast <= dt.timedelta(days=0)):
            report_date = blast + dt.timedelta(days=7)
        elif event - blast <= dt.timedelta(days=3):
            report_date = event
        else:
            report_date = event - dt.timedelta(days=2)
    if turn_weekday(report_date) == 5:
        report_date = report_date + dt.timedelta(days=2)
    if turn_weekday(report_date) == 6:
        report_date = report_date + dt.timedelta(days=1)

    return report_date


def turn_weekday(x):
    try:
        return x.weekday()
    except AttributeError:
        return None


if __name__ == '__main__':
    print(report_date_gen(None, None))
