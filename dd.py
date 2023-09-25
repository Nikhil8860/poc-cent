import datetime
date = '9/13/2023'
appointment_date = datetime.datetime.strptime(date, '%m/%d/%Y')
print(appointment_date)
