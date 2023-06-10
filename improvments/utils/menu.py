import os

from improvments.utils.time_diff import calculate_time_diff
from improvments.export.export_to_xlsx import create_and_save_excel
from improvments.handler.data_handler import get_input
from improvments.update.update_day import update_day
from improvments.update.update_config import modify_config


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def main_menu(data, config, signal_handler):
    calculate_time_diff(data)
    create_and_save_excel(data, config)
    print("\nMain Menu:")
    print("1. Enter a new job day")
    print("2. Update a specific job day")
    print("3. Modify config information")
    print("4. Exit")

    choice = input("Enter your choice: ")
    if choice == "1":
        get_input()
        calculate_time_diff(data)
        create_and_save_excel(data, config)
    elif choice == "2":
        update_day(data)
        calculate_time_diff(data)
        create_and_save_excel(data, config)
    elif choice == "3":
        modify_config(config)
    elif choice == "4":
        signal_handler(None, None, data)
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
