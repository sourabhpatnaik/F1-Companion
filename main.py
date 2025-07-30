import fastf1 as f1
from datetime import datetime

#Enabling Cache
f1.Cache.enable_cache('cache')


#UPCOMING RACES SCHEDULE 
def get_next_race():
    #Getting Today's Date and Year
    currentYear = datetime.today().year
    todayDate = datetime.today().date()

    #Current Year Schedule
    currentSchedule = f1.get_event_schedule(currentYear)

    # Iterating through Events and returning Next Event Details
    for _, event in currentSchedule.iterrows():
        event_date = event['EventDate'].to_pydatetime().date()

        if event_date > todayDate:
            # This is the next race
            print("Event Name: {}\nEvent Date: {}\nEvent Country: {}".format(event['EventName'], event_date, event['Country']))
            break

get_next_race()





