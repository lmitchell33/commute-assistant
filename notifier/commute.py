from datetime import datetime, timezone, timedelta
import requests

from config import GOOGLE_API_KEY, HOME_ADDRESS, WORK_ADDRESS
from notifier.logger import logger

GOOGLE_ROUTES_API_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

def get_commute_information(start_location, end_location, departure_time=None):
    """
    Gets commute time and some general/basic route information/directions from the Google Routes API.

    :param start_location: The starting address for the commute
    :param end_location: The ending address for the commute
    :param departure_time: Optional departure time, defaults to 7:30 AM today. Inputs can be:
    :return: A tuple containing the commute time (str), general route information/directions (str)
    """
    route_data = get_commute_route(start_location, end_location, departure_time)
    if not route_data:
        logger.error("No route data received")
        raise Exception("No route data received")
    
    routes = route_data.get("routes", [{}])[0]
    if not routes:
        logger.error("No routes found in the route data")
        raise Exception("No routes found in the route data")

    return get_commute_time(routes.get("duration", "0s")), get_general_route_info(routes.get("legs", [{}])[0].get("steps", []))


def get_commute_time(commute_duration):
    """
    Gets and calculates the commute time from the given route JSON. 
    Assumes the route is a valid response from the Google Routes API.
    
    :param route: Google Routes API response JSON  from routes/duration
    :return: String representing the commute time 
    """
    if not commute_duration:
        logger.error("Error finding commute time while calculating commute time.")
        raise Exception("Error finding commute time while calculating commute time.")

    time_seconds = int(commute_duration.rstrip("s"))
    if time_seconds == 0:
        logger.error("Error finding commute time. The route or duration of the route is empty or not valid")
        raise ValueError("Error finding commute time while calculating commute time.")
    
    hours = time_seconds // 3600
    minutes = (time_seconds % 3600) // 60
    seconds = time_seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        logger.warning("Something weird happened and the commute time is less than a minute.")
        return f"{seconds}s"


def get_general_route_info(directions, min_distance=100):
    """
    Gets a list of 'important' directions from the given route JSON. The only directions that are included in the
    output message are those that are longer than the given minimum distance (meters)
    
    :param directions: Google Routes API response JSON from routes/legs/steps
    :param min_distance: Minimum distance (meters) for a direction to be included in the output string
    :return: String '->' separated list of directions with a travel time greater than min_distance
    """
    if not directions:
        logger.error("Error finding commute route while calculating general route info.")
        raise Exception("Error finding commute route while calculating general route info.")
    
    steps_to_keep = [directions[0].get("navigationInstruction", {}).get("instructions", "")]

    for step in directions:
        # skip the smaller steps that are less than 100 meters because we just want to get the 
        # general idea behind the route 
        if int(step.get("distanceMeters")) < min_distance:
            continue

        instruction = step.get("navigationInstruction", {}).get("instructions", "")
        if instruction and instruction not in steps_to_keep:
            steps_to_keep.append(instruction)

    last_step = directions[-1].get("navigationInstruction", {}).get("instructions", "")
    if last_step not in steps_to_keep:
        steps_to_keep.append(directions[-1].get("navigationInstruction", {}).get("instructions", ""))

    if not steps_to_keep:
        logger.error("No steps found in the route directions")
        raise Exception("No steps found in the route directions")

    numbered_directions = [f"{i+1}. {direction}" for i, direction in enumerate(steps_to_keep)]

    return "\n".join(numbered_directions)


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
    url = f"{GOOGLE_ROUTES_API_URL}?key={GOOGLE_API_KEY}"

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


if __name__ == "__main__":
    commute_time, directions = get_commute_information(HOME_ADDRESS, WORK_ADDRESS, "23:30")
    print(f"Commute time: {commute_time}")
    print(f"Directions: \n {directions}")