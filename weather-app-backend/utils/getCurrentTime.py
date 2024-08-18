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

if __name__ == '__main__':
    current_time()    