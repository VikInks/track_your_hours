import datetime
import json
import os
import signal
import sys

import openpyxl
import pandas as pd
from openpyxl.styles import PatternFill

from utils.calculate_work_hours_and_difference import calculate_work_hours_and_difference
from utils.prompt import prompt_for_month, prompt_for_day, prompt_for_year
from utils.validate_input import validate_input

# Define RGB values for red, green, and yellow
RED = "FF0000"
GREEN = "00FF00"
YELLOW = "FFFF00"
WHITE = "FFFFFF"


class WorkHoursTracker:
    def __init__(self):
        try:
            with open('work_hours.json', 'r') as f:
                self.work_hours_data = json.load(f)
        except FileNotFoundError:
            self.work_hours_data = []

            # Print an error message or handle the exception appropriately
            print("work_hours.json file not found. Starting with an empty data list.")

    def recalculate_work_hours_difference(self):
        print("Recalculating work hours and difference...")
        """Recalculate the work hours and difference for all entries."""
        for entry in self.work_hours_data:
            # Calculate the work hours and difference
            updated_data_dict = calculate_work_hours_and_difference(
                entry["date"],
                entry["start_time"],
                datetime.timedelta(hours=int(entry["lunch_break"].split(":")[0]),
                                   minutes=int(entry["lunch_break"].split(":")[1])),
                entry["end_time"],
                entry["location"]
            )
            # Update the entry with the updated data
            entry.update(updated_data_dict)

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C interruption and save current data."""
        print('Interruption detected, saving data...')
        self.save_to_json()
        sys.exit(0)

    def save_to_json(self):
        """Save data to a JSON file."""
        # Ensure all keys are present in each dictionary in work_hours_data
        for entry in self.work_hours_data:
            for key in ["date", "day_of_week", "start_time", "lunch_break", "end_time", "location", "overtime",
                        "work_hours", "hours_diff"]:
                entry.setdefault(key, "")

        # Create a temporary file to avoid data loss in case of a crash during the write operation
        tempname = os.path.join(os.path.dirname('work_hours.json'), "tmp_" + os.path.basename('work_hours.json'))
        with open(tempname, 'w') as json_file:
            json.dump(self.work_hours_data, json_file, default=str)

        # Remove existing file if it exists
        if os.path.exists('work_hours.json'):
            os.remove('work_hours.json')

        # Rename temporary file to the final name
        os.rename(tempname, 'work_hours.json')

    def create_and_save_excel(self):
        # Create a pandas DataFrame from the work day details
        df = pd.DataFrame(self.work_hours_data,
                          columns=["date", "day_of_week", "start_time", "lunch_break", "end_time", "location",
                                   "overtime", "work_hours", "hours_diff"])

        # Format the 'date' column to datetime dd mm yyyy
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

        # Get the month name and year from the 'date' column
        month_year_name = df['date'].dt.strftime('%B %Y').iloc[0]

        # Save the DataFrame to an Excel file with the sheet name as the month name
        df.to_excel("work_hours.xlsx", index=False, sheet_name=str(month_year_name))

        # Load the Excel file
        wb = openpyxl.load_workbook("work_hours.xlsx")
        ws = wb[str(month_year_name)]

        # Apply formatting to the 'hours_diff' column
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=9, max_col=9):
            for cell in row:
                if cell.value is not None:
                    value_str = cell.value.strip('+ -')
                    if ':' in value_str:
                        hours, minutes = value_str.split(':')
                        value = float(hours) + float(minutes) / 60.0
                    else:
                        value = float(value_str)

                    if cell.value.startswith('-'):
                        value = -value

                    if value < 0:
                        fill = PatternFill(start_color=RED, end_color=RED, fill_type="solid")
                    elif value > 0:
                        fill = PatternFill(start_color=GREEN, end_color=GREEN, fill_type="solid")
                    else:
                        fill = PatternFill(start_color=WHITE, end_color=WHITE, fill_type="solid")

                    cell.fill = fill

                day_row = cell.row
                day_of_week = df.loc[day_row - 2, "day_of_week"]
                if day_of_week in ["Saturday", "Sunday"] and cell.value is not None and cell.value != 0:
                    for cell_in_row in ws[day_row]:
                        fill = PatternFill(start_color=YELLOW, end_color=YELLOW, fill_type="solid")
                        cell_in_row.fill = fill

        # Save the Excel file
        wb.save("work_hours.xlsx")

    def update_date_work_hours(self, selected_day: str, selected_month: str, selected_year: str):
        """Update the work hours for the given date."""
        if selected_month.__len__() == 1:
            selected_month = f"0{selected_month}"
        if selected_day.__len__() == 1:
            selected_day = f"0{selected_day}"

        date = f"{selected_year}-{selected_month}-{selected_day}"
        entry = next((item for item in self.work_hours_data if item["date"] == date), None)
        if entry is None:
            print("No data found for the selected date.")
            exit()
        # use validate_input() to get the updated data
        updated_data = validate_input(entry)
        # calculate the work hours and difference
        updated_data_dict = calculate_work_hours_and_difference(*updated_data)
        # update the entry with the updated data
        entry.update(updated_data_dict)

        if entry is None:
            print("No data found for the selected date.")
            return

    def run(self):
        """Main function to run the program."""
        signal.signal(signal.SIGINT, self.signal_handler)

        # Check for any incomplete entries
        incomplete_entry = next((entry for entry in self.work_hours_data if entry.get('status') == 'incomplete'), None)
        if incomplete_entry:
            print(f"Incomplete data detected for date {incomplete_entry['date']}. Please enter the missing data.")
            updated_data = validate_input(incomplete_entry)
            updated_data_dict = calculate_work_hours_and_difference(*updated_data)
            incomplete_entry.update(updated_data_dict)
            incomplete_entry['status'] = 'complete'

        self.recalculate_work_hours_difference()
        while True:
            # clear the console screen
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n1. Enter work hours")
            print("2. Modify work hours for a date")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                data = validate_input()
                data_dict = calculate_work_hours_and_difference(*data)
                if "day_of_week" not in data_dict:
                    date_datetime = datetime.datetime.strptime(data_dict["date"], "%Y-%m-%d")
                    data_dict["day_of_week"] = date_datetime.strftime("%A")
                data_dict['status'] = 'incomplete'
                self.work_hours_data.append(data_dict)
                self.save_to_json()
                data_dict['status'] = 'complete'
            elif choice == '2':
                selected_year = prompt_for_year()
                print("You selected: ", selected_year)
                selected_month = prompt_for_month()
                print("You selected: ", selected_month)
                selected_day = prompt_for_day()
                print("You selected: ", selected_day)
                self.update_date_work_hours(selected_day, selected_month, selected_year)
                self.save_to_json()
            elif choice == "3":
                self.save_to_json()
                self.create_and_save_excel()
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    tracker = WorkHoursTracker()
    tracker.run()
