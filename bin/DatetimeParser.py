from datetime import datetime


true_dt_format = '%Y/%m/%d %H:%M'


dt_format_list = [
    '%Y%m%d%H%M',
    'm%d%H%M',
    '%Y.%m.%d %H.%M',
    '%Y.%m.%d %H:%M',
    '%Y.%m.%d %H%M',
    '%Y.%m.%d',
    '%Y/%m/%d %H.%M',
    '%Y/%m/%d %H:%M',
    '%Y/%m/%d %H%M',
    '%Y/%m/%d',
    '%m/%d %H.%M',
    '%m/%d %H:%M',
    '%m/%d %H%M',
    '%m/%d'
]
only_time_list = [
    '%H.%M',
    '%H:%M',
    '%H%M'
]


def parse_datetime(string):
    dt = None
    for dt_format in dt_format_list:
        try:
            dt = datetime.strptime(string, dt_format)
            break
        except ValueError:
            pass
    if dt is not None:
        if dt.year == 1900:
            dt = dt.replace(year=dt.now().year)
        return dt
    for dt_format in only_time_list:
        try:
            dt = datetime.strptime(string, dt_format)
            break
        except ValueError:
            pass
    if dt is not None:
        dt = dt.replace(year=dt.now().year, month=dt.now().month, day=dt.now().day)
    return dt





def get_readable(dt):
    readable = ''
    if dt.year != 1900:
        readable += f'{dt.year}年'
    else:
        dt = dt.replace(year=dt.now().year)
    readable += f'{dt.month}月{dt.day}日'
    if dt.hour or dt.minute:
        readable += f' {dt.hour}點{dt.minute}分'
    return readable

