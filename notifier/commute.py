from config import GOOGLE_API_KEY, HOME_ADDRESS, WORK_ADDRESS
from datetime import datetime, timezone, timedelta
from notifier.logger import logger
import requests
import json

GOOGLE_ROUTES_API_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

def get_commute_time(route):
    if not route:
        return


def get_general_route_info(route):
    if not route:
        return 


def get_commute_route(start_location, end_location, departure_time=None):
    """
    Gets possible routes to take from the given starting location (address) 
    to the given ending location (address) using the Google Routes API

    The given format for the address is a string such as:
    "1234 Example Street, City, State Zip Code"

    This address can be as extensive or as simple as you want, but
    the more specific the address the more accurate th results

    :param start_location:  The starting address for the commute
    :param end_location: The ending address for the commute
    :param departure_time: Optional departure time, defaults to 7:30 AM today. Inputs can be:
    :type departure_time: datetime, str (HH:MM), or None (default)
    :return: A JSON response containing the routes and their details
    """
    # TODO: update structure of this function
    headers = {
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "routes.duration,routes.legs.steps"
    }

    departure_time = get_rfc3339_time(departure_time)

    # if you want you can also add "computeAlternativeRoutes" : True, to get more routes
    request_body = {
        "origin" : {
            "address": start_location
        },
        "destination" : {
            "address": end_location
        },
        "travelMode" : "DRIVE",
        "routingPreference" : "TRAFFIC_AWARE_OPTIMAL",
        "departureTime" : departure_time,
        "languageCode": "en-US",
        "units": "METRIC",
        "trafficModel" : "BESt_GUESS",
    }
    
    url = f"{GOOGLE_ROUTES_API_URL}?key={GOOGLE_API_KEY}"

    response = requests.post(
        url=url, 
        json=request_body, 
        headers=headers
    )

    if not response.ok:
        logger.error(f"Failed to get commute route: {response.status_code} - {response.text}")
        raise Exception(f"Failed to get commute route: {response.status_code} - {response.text}")
    
    return response.json()

def get_rfc3339_time(time="07:30"):
    """
    Converts a given time to RFC3339 format in UTC.

    :param time: The time to convert, either a string in HH:MM format or a datetime object.
    :type time: str or datetime, optional
    :return: The time in RFC3339 format in UTC.
    """

    # set the timezone to EST because that is where I live
    est_timezone = timezone(timedelta(hours=-5)) 
    if isinstance(time, str):
        if len(time) != 5 or time[2] != ":":
            logger.error("Failed to convert time to RFC3339 format. Inputted string time must be in HH:MM format.")
            raise ValueError("Time must be in HH:MM format")
        
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        today = datetime.today().date()
        est_time = datetime(today.year, today.month, today.day, hour, minute, 0, 000000, tzinfo=est_timezone)

    elif isinstance(time, datetime):
        # need to ensure the timezone is set to EST (my time sorry other people)
        if time.tzinfo is None:
            est_time = time.replace(tzinfo=est_timezone)
        else:
            est_time = time.astimezone(est_timezone)

    # timezones are created in EST to ensure consistency with local time, but api requires UTC
    utc_time = est_time.astimezone(timezone.utc)
    return utc_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


print(json.dumps(get_commute_route(HOME_ADDRESS, WORK_ADDRESS, "20:30")))