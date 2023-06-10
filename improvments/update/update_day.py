from improvments.handler.data_handler import get_time_input


def update_day(data):
    date = input("Enter the date of the job day you want to update (YYYY-MM-DD): ")
    year, month, day = map(int, date.split('-'))

    if str(year) in data and str(month) in data[str(year)] and str(day) in data[str(year)][str(month)]:
        print("Enter the new times for this day. Leave blank to keep the current time.")
        data[str(year)][str(month)][str(day)]["location"] = input("Enter new location (home/office): ") or data[str(year)][str(month)][str(day)]["location"]

        data[str(year)][str(month)][str(day)] = {
            "start_job": get_time_input("Enter new starting job hour (HH:MM or HH): ") or
                         data[str(year)][str(month)][str(day)]["start_job"],
            "start_break": get_time_input("Enter new starting break hour (HH:MM or HH): ") or
                           data[str(year)][str(month)][str(day)]["start_break"],
            "end_break": get_time_input("Enter new end break hour (HH:MM or HH): ") or
                         data[str(year)][str(month)][str(day)]["end_break"],
            "end_job": get_time_input("Enter new ending job hour (HH:MM or HH): ") or
                       data[str(year)][str(month)][str(day)]["end_job"]
        }
    else:
        print("No data found for this date.")

