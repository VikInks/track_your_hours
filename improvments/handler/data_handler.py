import datetime
from collections import defaultdict

from improvments.utils.get_time_input import get_time_input

# Define the structure of the data to be saved
data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

# Define a configuration file path






def get_input():
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    if not date:
        date = datetime.date.today().isoformat()

    year, month, day = map(int, date.split('-'))
    current_date = datetime.date(year, month, day)

    location = input("Enter location (home/office): ")
    start_job = get_time_input("Enter starting job hour (HH:MM or HH): ")
    start_break = get_time_input("Enter starting break hour (HH:MM or HH): ")
    end_break = get_time_input("Enter end break hour (HH:MM or HH): ")
    end_job = get_time_input("Enter ending job hour (HH:MM or HH): ")

    data[str(current_date.year)][str(current_date.month)][str(current_date.day)] = {
        "location": location,
        "start_job": start_job,
        "start_break": start_break,
        "end_break": end_break,
        "end_job": end_job
    }


