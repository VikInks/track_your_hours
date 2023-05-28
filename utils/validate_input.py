import datetime


def validate_input(date=None):
    """Validate user input and return formatted data."""
    while True:
        if date is None:
            date = input("Enter the date (yyyy-mm-dd) or press Enter to use today's date: ")
        start_time = input("Enter start time (HH:MM): ")
        lunch_break = input("Enter duration of lunch break (HH:MM) or press Enter if no break: ")
        end_time = input("Enter end time (HH:MM): ")
        location = input("Enter work location (Office or Home): ").lower()
        additional_break = input("Enter duration of additional break (HH:MM) or press Enter if no break: ")

        try:
            if date == "":
                date = datetime.datetime.now().strftime("%Y-%m-%d")
            else:
                if isinstance(date, dict):
                    date = date['date']
                datetime.datetime.strptime(date, "%Y-%m-%d")

            datetime.datetime.strptime(start_time, "%H:%M")
            if lunch_break == "":
                lunch_break = "0:00"
            lunch_break_td = datetime.timedelta(hours=int(lunch_break.split(':')[0]), minutes=int(lunch_break.split(':')[1]))
            datetime.datetime.strptime(end_time, "%H:%M")
            if additional_break == "":
                additional_break = "0:00"
            additional_break_td = datetime.timedelta(hours=int(additional_break.split(':')[0]), minutes=int(additional_break.split(':')[1]))
            lunch_break_td += additional_break_td

            if location not in ["office", "home"]:
                raise ValueError

            return date, start_time, lunch_break_td, end_time, location
        except ValueError:
            print("Invalid input. Please re-enter the details correctly.")
