import datetime
import json

config_json_path = "config.json"

with open(config_json_path) as f:
    config = json.load(f)

full_time_hours = int(config["full_time_hours"])
daily_percentage = float(config["daily_percentage"]) / 100


def format_time_diff(time_diff):
    sign = "-" if time_diff < 0 else ""
    hours = int(time_diff)
    minutes = int((abs(time_diff) * 60) % 60)
    return f"{sign}{abs(hours)}:{minutes:02d}"


def calculate_time_diff(data):
    for year, months in data.items():
        for month, days in months.items():
            for day, times in days.items():
                start_job = datetime.datetime.strptime(times["start_job"], "%H:%M")
                end_job = datetime.datetime.strptime(times["end_job"], "%H:%M")
                start_break = datetime.datetime.strptime(times["start_break"], "%H:%M")
                end_break = datetime.datetime.strptime(times["end_break"], "%H:%M")

                work_time = ((end_job - start_job) - (end_break - start_break)).total_seconds() / 3600
                target_time = full_time_hours * daily_percentage

                # check if the day is a weekend day
                if datetime.datetime(int(year), int(month), int(day)).weekday() in [5, 6]:
                    time_diff = work_time
                else:
                    time_diff = work_time - target_time

                if times["location"] == "office":
                    time_diff = 0

                times["time_diff"] = format_time_diff(time_diff)
                # if the time difference is negative, the employee is under the target time and over if positive or
                # "" if 0
                times["under_or_over"] = "over" if time_diff > 0 else "under" if time_diff < 0 else ""
