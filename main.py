import fastf1 as f1
from datetime import datetime
from tabulate import tabulate

#Enabling Cache
f1.Cache.enable_cache('cache')


#****************************** UPCOMING RACES SCHEDULE ****************************** 

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

# get_next_race()


#****************************** CURRENT SEASON DRIVER' S STANDING ******************************

def get_current_Driverstanding():
    """
    Return cumulative driver standings for current season.
    Output: list of dicts sorted by points (highest first)
    """
    
    currentYear = datetime.today().year
    todayDate = datetime.today().date()
    currentSchedule = f1.get_event_schedule(currentYear)
    
    completedRace = []
    
    for index, event in currentSchedule.iterrows():
        # ---- FIX 1: Skip testing events ----
        if event['EventFormat'] == "testing":   # <-- NEW LINE
            continue

        event_date = event['EventDate'].to_pydatetime().date()
        
        if event_date < todayDate:
            completedRace.append(event['RoundNumber'])

    standings = {}
    
    #Loading Race Sessions
    for round_number in completedRace:
        session = f1.get_session(currentYear,round_number, 'R')
        session.load()
        results = session.results

        for index, driver in results.iterrows():
            code = driver['Abbreviation']
            name = driver['FullName']
            teamName = driver['TeamName']
            point = driver['Points']
            
            if code not in standings:
                standings[code] = {"name": name,
                                   "Team": teamName,
                                   "points": 0}
            standings[code]["points"] += point 
    
    sorted_standings = sorted(standings.values(), key=lambda x: x['points'], reverse=True)
    
    table_data = []
    for i, driver in enumerate(sorted_standings, start=1):
        table_data.append([i, driver['name'], driver['Team'], driver['points']])
    print(tabulate(table_data, headers=["Pos", "Driver", "Team", "Points"], tablefmt="pretty"))
