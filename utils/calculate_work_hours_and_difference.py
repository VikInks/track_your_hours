import datetime
from typing import Dict, Union


def calculate_work_hours_and_difference(date: str, start_time: str, lunch_break: datetime.timedelta, end_time: str, location: str) -> Dict[str, Union[float, str]]:
    """Calculate work hours and the difference from standard work hours."""
    date_datetime = datetime.datetime.strptime(date, "%Y-%m-%d")
    day_of_week = date_datetime.strftime("%A")
    is_weekend = day_of_week in ['Saturday', 'Sunday']
    data_dict = {"date": date, "day_of_week": day_of_week, "start_time": start_time, "lunch_break": str(lunch_break), "end_time": end_time, "location": location, "overtime": is_weekend}

    FMT = "%H:%M"
    start_time = datetime.datetime.strptime(start_time, FMT)
    end_time = datetime.datetime.strptime(end_time, FMT)

    work_duration = (end_time - start_time) - lunch_break
    work_hours = work_duration.seconds / 3600.0

    standard_work_hours = 8.0 if not is_weekend else 0.0
    hours_diff = work_hours - standard_work_hours

    sign = '-' if hours_diff < 0 else '+'
    hours_diff_str = f"{sign} {abs(int(hours_diff)):02d}:{abs(int((hours_diff * 60) % 60)):02d}"

    if location == "office":
        work_hours = 8.0
        hours_diff_str = f"{0 // 3600:02d}:{(0 // 60) % 60:02d}"

    data_dict.update({"work_hours": work_hours, "hours_diff": hours_diff_str})
    return data_dict
