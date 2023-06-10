import json


def modify_config(config):
    print("\nConfig Menu:")
    print("1. Modify full time hours")
    print("2. Modify daily percentage")
    print("3. Return to main menu")

    choice = input("Enter your choice: ")
    if choice == "1":
        full_time_hours = input("Enter new full time hours: ")
        config["full_time_hours"] = full_time_hours
    elif choice == "2":
        daily_percentage = input("Enter new daily percentage: ")
        config["daily_percentage"] = daily_percentage
    elif choice == "3":
        return
    else:
        print("Invalid choice. Please enter a number between 1 and 3.")

    # Writing the updated config back to the file
    with open('config.json', 'w') as f:
        json.dump(config, f)
