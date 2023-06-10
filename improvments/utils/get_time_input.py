from improvments.utils.time_pattern import time_pattern


def get_time_input(prompt):
    while True:
        time_input = input(prompt)
        if time_pattern.match(time_input):
            if ":" not in time_input:
                time_input += ":00"
            return time_input
        print("Invalid input. Please enter time in the format HH:MM or HH.")