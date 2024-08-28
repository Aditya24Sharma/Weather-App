from datetime import datetime
import pytz

# Description: Give current time based on timezone
# Arguments: Time Zone
# Returns time in H:M format in string
def current_time(currenttimezone = 'America/New_York'):
    timezone = pytz.timezone(currenttimezone)
    timeInTimezone = datetime.now(timezone)
    formattedTime = timeInTimezone.strftime("%H:%M")
    return formattedTime

def todays_date(currenttimezone = 'America/New_York'):
    timezone = pytz.timezone(currenttimezone)
    DateInTimezone = datetime.now(timezone)
    formattedDate = DateInTimezone.strftime("%-d %b, %Y")
    return formattedDate

if __name__ == '__main__':
    current_time()    