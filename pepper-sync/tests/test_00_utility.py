
from datetime import datetime
from pepper.utils import parse_date_time


def test_date_time_paser():
    parsed = parse_date_time("01-01-2001 00:00:00", "%d-%m-%Y %H:%M:%S")
    assert parsed == datetime(2001, 1, 1, 0, 0, 0)
