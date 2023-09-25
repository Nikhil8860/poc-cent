from datetime import datetime


def get_formatted_date(date):
    appointment_date = datetime.strptime(date, '%m/%d/%Y %I:%M %p')
    # appointment_date = appointment_date.strftime("%m/%d/%Y")
    return appointment_date


def get_current_date():
    current_datetime = datetime.now()

    # getting the date and time from the current date and time in the given format
    # current_date_time = current_datetime.strftime("%m/%d/%Y")
    return current_datetime


def get_difference(appointment_date):
    appointment_date = get_formatted_date(date=appointment_date)
    current_date = get_current_date()
    delta = appointment_date - current_date
    sec = delta.total_seconds()
    hours = sec / (60 * 60)
    return hours


if __name__ == '__main__':
    d1 = get_formatted_date('09/19/2023 5:59 PM')
    print(d1)
    d2 = get_current_date()
    print(d2)
    print(get_difference('09/19/2023 5:59 PM'))
