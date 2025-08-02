import fastf1 as f1
import requests
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import logging
import livef1
from fastf1.ergast import Ergast

# Initialize Ergast API
ergast = Ergast()

# Suppress FastF1 debug logs
logging.getLogger("fastf1").setLevel(logging.ERROR)

# ------------------ ENABLE FASTF1 CACHE ------------------
# This speeds up data loading by caching previous requests locally
f1.Cache.enable_cache('cache')

# ------------------ OPENF1 API BASE URL ------------------
openf1API_Url = "https://api.openf1.org/v1/"

# (Optional) Check API availability
f1Api = requests.get(openf1API_Url).json()

# =========================================================
#                    UPCOMING RACE SCHEDULE
# =========================================================
def get_next_race():
    """
    Fetch the next upcoming race of the current season.
    Uses FastF1 schedule data and compares with today's date.
    """
    currentYear = datetime.today().year
    todayDate = datetime.today().date()

    # Get full event schedule for the current year
    currentSchedule = f1.get_event_schedule(currentYear)

    # Loop through events and find the first future event
    for _, event in currentSchedule.iterrows():
        event_date = event['EventDate'].to_pydatetime().date()

        if event_date > todayDate:
            # Return next race details
            result = (
                f"**🏁\xa0   Event Name:** {event['EventName']}\n\n"
                f"**📅\xa0   Event Date:** {event_date}\n\n"
                f"**🌍\xa0   Event Country:** {event['Country']}"
            )
            return result


# =========================================================
#               CURRENT SEASON DRIVER STANDINGS
# =========================================================
def get_current_Driverstanding(year=None):
    """
    Calculate and return driver standings for the given season.
    Defaults to current year if not provided.
    """
    currentYear = datetime.today().year
    if year is None:
        year = currentYear

    final_data = []
    driver_data = ergast.get_driver_standings(season=year, result_type='raw')

    if not driver_data or 'DriverStandings' not in driver_data[0]:
        return "No standings data available for this year."

    driver_list = driver_data[0]['DriverStandings']
    driverData = pd.json_normalize(driver_list)

    for _, rows in driverData.iterrows():
        final_data.append([
            rows['position'],
            rows['Driver.givenName'] + " " + rows['Driver.familyName'],
            rows['wins'],
            rows['points'],
            rows['Driver.nationality']
        ])

    result = tabulate(
        final_data,
        headers=["Position", "Driver Name", "Wins", "Points", "Nationality"],
        tablefmt="pretty"
    )
    return result


# =========================================================
#                    FULL SEASON SCHEDULE
# =========================================================
def get_full_seasonSchedule():
    """
    Return the full season race schedule in a tabular format.
    """
    table_data = []
    currentYear = datetime.today().year

    # Get schedule for current year
    schedule = f1.get_event_schedule(currentYear)

    # Iterate and extract relevant event info
    for i in range(len(schedule['RoundNumber'])):
        roundNumber = schedule['RoundNumber'][i]
        eventName = schedule['OfficialEventName'][i]
        eventDate = schedule['EventDate'][i].strftime("%Y-%m-%d")
        country = schedule['Country'][i]
        location = schedule['Location'][i]

        table_data.append([roundNumber, eventName, eventDate, location, country])

    # Return formatted table
    return tabulate(
        table_data,
        headers=["Round", "Event Name", "Event Date", "Country", "Location"],
        tablefmt="pretty"
    )


# =========================================================
#                    DRIVER DETAILS (Ergast)
# =========================================================
def get_DriverDetails(drivername=None):
    """
    Fetch driver details from OpenF1 API based on driver name.
    (Currently incomplete - needs implementation)
    """
    try:
        driver_info = ergast.get_driver_info(season='current', result_type='raw')
        driverData = pd.DataFrame(driver_info)
        print(driverData)
        # Implementation pending: Filter and format driver details
    except:
        pass


# =========================================================
#                    CONSTRUCTOR STANDINGS
# =========================================================
def get_constructor_standings(year=None):
    """
    Return constructor standings for the given season.
    Defaults to current year if not provided.
    """
    currentYear = datetime.today().year
    if year is None:
        year = currentYear

    final_data = []
    constructor_data = ergast.get_constructor_standings(season=year, result_type='raw')

    if not constructor_data or 'ConstructorStandings' not in constructor_data[0]:
        return "No standings data available for this year."

    standings_list = constructor_data[0]['ConstructorStandings']
    standingData = pd.json_normalize(standings_list)

    for _, rows in standingData.iterrows():
        final_data.append([
            rows['position'],
            rows['Constructor.name'],
            rows['wins'],
            rows['points'],
            rows['Constructor.nationality']
        ])

    result = tabulate(
        final_data,
        headers=["Position", "Team Name", "Total Wins", "Total Points", "Team Nationality"],
        tablefmt="pretty"
    )
    return result

# #---------------------------------------------------------

# from livef1.adapters.realtime_client import RealF1Client

# client = RealF1Client(
#     topics=["CarData.z", "SessionInfo","TrackInfo"],
#     log_file_name="./output.json"  # Optional: log incoming data
# )

# @client.callback("basic_handler")
# async def handle_data(records):
#     print(records)

# import datetime

# @client.callback("log_handler")
# async def log_with_timestamp(records):
#     with open("data_with_timestamp.log", "a") as f:
#         for record in records:
#             timestamp = datetime.datetime.now().isoformat()
#             f.write(f"{timestamp} - {record}\n")
    

# client.run()

# =========================================================
#                    DETAILED SCHEDULE
# =========================================================

def get_fullRacesession_Info(country = None, year = None):
    
    
    if country is None and year is None:
        return f"Please Provide a Valid Country and Year."
    
    session_url = "https://api.openf1.org/v1/sessions?"
    parameters = {
        'country_name': country,
        'year': year,
    }
    
    session_info = requests.get(session_url,params=parameters)
    session_data = session_info.json()
    print(session_data)

# print(get_fullRacesession_Info('Belgium',2024))