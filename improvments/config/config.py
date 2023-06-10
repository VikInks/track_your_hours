import json
import os


def check_config(config_file):
    if not os.path.exists(config_file):
        while True:
            full_time_hours = input("Please enter how many hours of work is a full time job: ")
            if full_time_hours.isdigit() and 0 <= int(full_time_hours) <= 24:
                break
            print("Invalid input. Please enter a number between 0 and 24.")
        while True:
            daily_percentage = input("Please enter at which percentage you are working daily: ")
            if daily_percentage.isdigit() and 0 <= int(daily_percentage) <= 100:
                break
            print("Invalid input. Please enter a number between 0 and 100.")
        with open(config_file, 'w') as f:
            json.dump({"full_time_hours": full_time_hours, "daily_percentage": daily_percentage}, f)
