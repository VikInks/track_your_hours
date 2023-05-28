from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


def prompt_for_year():
    years = list(map(str, range(2023, 2050)))

    completer = WordCompleter(years, ignore_case=True)

    selected_year = prompt("Please select a year: ", completer=completer)
    return selected_year


def prompt_for_month():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    months_number = list(map(str, range(1, 13)))
    completer = WordCompleter(months, ignore_case=True)
    months_dict = dict(zip(months, months_number))
    selected_month = prompt("Please select a month: ", completer=completer)
    return months_dict[selected_month]


def prompt_for_day():
    days = list(map(str, range(1, 32)))

    completer = WordCompleter(days, ignore_case=True)

    selected_day = prompt("Please select a day: ", completer=completer)
    return selected_day
