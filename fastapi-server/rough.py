from datetime import date, timedelta

RECENT_YEARS = 3

today = date.today()

timeD =  timedelta(days=365 * RECENT_YEARS)

from_date = today - timedelta(days=365 * RECENT_YEARS)

print(today)
print(timeD)