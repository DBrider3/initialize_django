# System
import datetime
import pytz


def get_now(tz="UTC"):
    """
    return timezone aware datetime
    """
    if tz == "UTC":
        return datetime.datetime.now(datetime.timezone.utc)

    # UTC 제외한 timezone에 대한 처리
    assert tz in pytz.all_timezones

    return datetime.datetime.now(pytz.timezone(tz))
