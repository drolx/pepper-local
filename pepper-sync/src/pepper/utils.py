import os
import sys
from datetime import datetime, time

today = datetime.today()
start_of_day = datetime.combine(today, time.min)
end_of_day = datetime.combine(today, time.max)


def parse_date_time(date_string: str, format: str = "%d-%m-%Y %H:%M:%S") -> datetime:
    parsed_datetime = datetime.strptime(date_string, format)

    return parsed_datetime


def get_process_path(requested_path: str = ""):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, requested_path)

def list_subclass_names(cls):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    subclasses = cls.__subclasses__()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    all_class_names = [cl.__name__ for cl in subclasses]  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    return all_class_names  # pyright: ignore[reportUnknownVariableType]

