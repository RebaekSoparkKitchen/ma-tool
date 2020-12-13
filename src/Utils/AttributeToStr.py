import datetime as dt


def transfer(obj):
    col = []
    values = []
    for name, value in vars(obj).items():
        if isinstance(value, dt.datetime):
            value = value.strftime("%Y-%m-%d %H:%M:%S")
        col.append(name[1:])
        values.append(value)
    return tuple(col), tuple(values)
