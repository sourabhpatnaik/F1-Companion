import fastf1 as f1
import requests
import pandas as pd
from datetime import datetime
from tabulate import tabulate
import logging
from fastf1.ergast import Ergast

# =========================================================
#                   INITIAL SETUP
# =========================================================

# Initialize Ergast API
ergast = Ergast()

# Suppress FastF1 debug logs
logging.getLogger("fastf1").setLevel(logging.ERROR)

# Enable FastF1 cache (speeds up repeated data loads)
f1.Cache.enable_cache('cache')

# OpenF1 API base URL
openf1API_Url = "https://api.openf1.org/v1/"

# (Optional) Check API availability
f1Api = requests.get(openf1API_Url).json()


# =========================================================
#                   UPCOMING RACE SCHEDULE
# =========================================================
def get_next_race():
    """
    Fetch the next upcoming race of the current season.
    Uses FastF1 schedule data and compares with today's date.

    Returns:
        str: Formatted string containing event name, date, and country.
    """
    currentYear = datetime.today().year
    todayDate = datetime.today().date()

    # Get full event schedule for the current year
    currentSchedule = f1.get_event_schedule(currentYear)

    # Find the first future event
    for _, event in currentSchedule.iterrows():
        event_date = event['EventDate'].to_pydatetime().date()

        if event_date > todayDate:
            return (
                f"🏁 **Event Name:** {event['EventName']}\n\n"
                f"📅 **Event Date:** {event_date}\n\n"
                f"🌍 **Event Country:** {event['Country']}"
            )


# =========================================================
#               CURRENT SEASON DRIVER STANDINGS
# =========================================================
def get_current_Driverstanding(year=None):
    """
    Get driver standings for the given season.

    Args:
        year (int, optional): Year of the season. Defaults to current year.

    Returns:
        str: Driver standings in table format.
    """
    if year is None:
        year = datetime.today().year

    final_data = []
    driver_data = ergast.get_driver_standings(season=year, result_type='raw')

    if not driver_data or 'DriverStandings' not in driver_data[0]:
        return "❌ No standings data available for this year."

    driver_list = driver_data[0]['DriverStandings']
    driverData = pd.json_normalize(driver_list)

    for _, rows in driverData.iterrows():
        final_data.append([
            rows['position'],
            f"{rows['Driver.givenName']} {rows['Driver.familyName']}",
            rows['wins'],
            rows['points'],
            rows['Driver.nationality']
        ])

    return tabulate(
        final_data,
        headers=["Position", "Driver Name", "Wins", "Points", "Nationality"],
        tablefmt="pretty"
    )


# =========================================================
#                   FULL SEASON SCHEDULE
# =========================================================
def get_full_seasonSchedule():
    """
    Get the full season race schedule.

    Returns:
        str: Table of all race events for the current season.
    """
    table_data = []
    currentYear = datetime.today().year
    schedule = f1.get_event_schedule(currentYear)

    for i in range(len(schedule['RoundNumber'])):
        table_data.append([
            schedule['RoundNumber'][i],
            schedule['OfficialEventName'][i],
            schedule['EventDate'][i].strftime("%Y-%m-%d"),
            schedule['Location'][i],
            schedule['Country'][i]
        ])

    return tabulate(
        table_data,
        headers=["Round", "Event Name", "Event Date", "Country", "Location"],
        tablefmt="pretty"
    )


# =========================================================
#                   DRIVER DETAILS (Ergast)
# =========================================================
def get_DriverDetails(drivername=None, Season=None):
    """
    Fetch driver details from OpenF1 API.

    Args:
        drivername (str): Driver's name, code, or number.
        Season (str or int): Season year.

    Returns:
        str: Driver information formatted with emojis.
    """
    try:
        if not drivername or not Season:
            drivername = input("Enter Driver Name or Code: ")
            Season = input("Enter Season: ")
            # return "❌ Error: Missing driver code/name or season."

        drivername = str(drivername).strip().lower()
        Season = str(Season).strip()

        driver_info = ergast.get_driver_info(season=Season, result_type='raw')
        driverData = pd.DataFrame(driver_info)

        if driverData.empty:
            return f"⚠ No driver data found for season {Season}."

        for _, data in driverData.iterrows():
            code = str(data.get('code', '') or '').lower()
            number = str(data.get('permanentNumber', '') or '').lower()
            fullName = f"{data.get('givenName', '')} {data.get('familyName', '')}".strip()
            fullNameLower = fullName.lower()

            if drivername in (code, number, fullNameLower):
                dob = data.get('dateOfBirth', '')
                dob = dob.strftime('%Y-%m-%d') if pd.notnull(dob) else 'N/A'

                return (
                    f"🏎 **Driver Details ({Season})**\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"👤 Name: {fullName}\n"
                    f"🎂 DOB: {dob}\n"
                    f"🌍 Nationality: {data.get('nationality', 'N/A')}\n"
                    f"🔤 Driver Code: {code.upper() or 'N/A'}\n"
                    f"🔢 Number: {number or 'N/A'}\n"
                    f"🆔 Driver ID: {data.get('driverId', 'N/A')}\n"
                    f"━━━━━━━━━━━━━━━━━━"
                )

        return f"⚠ No driver found matching '{drivername}' in {Season}."

    except Exception as e:
        return f"❌ Error: {e}"


# =========================================================
#                   CONSTRUCTOR STANDINGS
# =========================================================
def get_constructor_standings(year=None):
    """
    Get constructor standings for the given season.

    Args:
        year (int, optional): Year of the season. Defaults to current year.

    Returns:
        str: Constructor standings in table format.
    """
    if year is None:
        year = datetime.today().year

    final_data = []
    constructor_data = ergast.get_constructor_standings(season=year, result_type='raw')

    if not constructor_data or 'ConstructorStandings' not in constructor_data[0]:
        return "❌ No standings data available for this year."

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

    return tabulate(
        final_data,
        headers=["Position", "Team Name", "Total Wins", "Total Points", "Team Nationality"],
        tablefmt="pretty"
    )


# =========================================================
#                   DETAILED SESSION SCHEDULE
# =========================================================
def get_fullRacesession_Info(country=None, year=None):
    """
    Get detailed session info for a given country and year.

    Args:
        country (str, optional): Country name.
        year (int or str, optional): Season year.

    Returns:
        str: Table with session details.
    """
    if country is None and year is None:
        country = input("Enter Country: ").title()
        year = input("Enter Year: ")

    parameters = {'country_name': country, 'year': year}
    session_info = requests.get("https://api.openf1.org/v1/sessions?", params=parameters)
    session_data = session_info.json()
    testdata = pd.DataFrame(session_data)

    final_arr = []
    for _, row in testdata.iterrows():
        start_dt = datetime.fromisoformat(row['date_start'])
        end_dt = datetime.fromisoformat(row['date_end'])
        final_arr.append([
            row['country_name'],
            row['location'],
            row['session_name'],
            row['session_type'],
            start_dt.date(),
            start_dt.time(),
            end_dt.time()
        ])

    sortedData = pd.DataFrame(final_arr, columns=[
        'Country', 'Location', 'Session Name', 'Session Type', 'Date', 'Start Time', 'End Time'
    ])

    return tabulate(
        sortedData.values,
        headers=['Country', 'Location', 'Session Name', 'Session Type', 'Date', 'Start Time', 'End Time'],
        tablefmt='pretty'
    )


# =========================================================
#                   LAST RACE RESULT
# =========================================================
def recentRaceResult():
    """
    Get the results of the most recent race.

    Returns:
        str: Table containing position, driver name, laps, points, and gap to leader.
    """
    race_params = {'session_key': 'latest'}

    race_df = pd.DataFrame(requests.get(
        "https://api.openf1.org/v1/session_result?", params=race_params
    ).json())

    driver_df = pd.DataFrame(requests.get(
        "https://api.openf1.org/v1/drivers?", params=race_params
    ).json())

    merged_df = race_df.merge(
        driver_df[['driver_number', 'full_name']],
        on='driver_number',
        how='left'
    )

    final_data = []
    for _, info in merged_df.iterrows():
        position = int(info['position']) if pd.notna(info['position']) else "DNF"
        final_data.append([
            position,
            info['full_name'],
            info['number_of_laps'],
            info['points'],
            info['gap_to_leader']
        ])

    sortedData = pd.DataFrame(final_data, columns=[
        'Position', 'Name', 'Laps', 'Points', 'Gap to Leader'
    ])
    sortedData['Position'] = pd.Categorical(sortedData['Position'], ordered=True)
    sortedData = sortedData.sort_values(
        by='Position',
        key=lambda col: col.map(lambda x: float('inf') if x == 'DNF' else x)
    )

    return tabulate(
        sortedData.values,
        headers=['Position', 'Name', 'Laps', 'Points', 'Gap to Leader (s)'],
        tablefmt="pretty"
    )
