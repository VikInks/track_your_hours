def validate_and_sort_data(data):
    sorted_data = {}

    for year, months in data.items():
        sorted_data[year] = {}

        for month, days in months.items():
            sorted_data[year][month] = {}

            for day, times in days.items():
                sorted_data[year][month][day] = times

            # Sort days within the month
            sorted_data[year][month] = dict(sorted(sorted_data[year][month].items(), key=lambda x: int(x[0])))

        # Sort months within the year
        sorted_data[year] = dict(sorted(sorted_data[year].items(), key=lambda x: int(x[0])))

    # Sort years
    sorted_data = dict(sorted(sorted_data.items(), key=lambda x: int(x[0])))

    return sorted_data
