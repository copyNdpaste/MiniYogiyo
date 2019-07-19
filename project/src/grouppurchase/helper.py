import datetime

DEADLINE_PERIOD = 10


def set_deadline():
    now_date = datetime.datetime.now()
    result = now_date + datetime.timedelta(days=DEADLINE_PERIOD)
    return result
