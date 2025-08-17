"""
Main script for the project. I could add a shebang at the top of this file that would let me run it
in the cronjob without declaring the python interpreter, but I like to keep it explicit. 
"""
from argparse import ArgumentParser

from notifier.commute import get_commute_information
from notifier.message import send_sms_message
from notifier.logger import logger
from config import PHONE_NUMBER, GMAIL_ADDRESS

def construct_commute_message(start_addr: str, end_addr: str, departure_time: str, travel_method: str):
    """
    Construct the SMS message to send to the user

    :param start_addr: The starting address for the commute
    :param end_addr: The ending address for the commute
    :param departure_time: Optional departure time, defaults to 7:30 AM today.
    :param travel_method: Optional departure time, defaults to 7:30 AM today.
    :return: The final SMS message
    """
    travel_time , directions = get_commute_information(start_addr, end_addr, travel_method, departure_time, )
    
    # the verizon SMS gateway kept truncating the message because it was too long, so
    # shorter the address to use less characters 
    start_addr = start_addr.split(",")[0]
    end_addr = end_addr.split(",")[0]

    final_msg = f"Your commute today is {travel_time} from {start_addr} to {end_addr}. Here is the optimal route: \n\n{directions}"
    return final_msg


def parse_args():
    """
    Creates and parses CLI arguments
    """
    # only make the argument required if the environment variable is not set
    parser = ArgumentParser(description="Send commute information via SMS")
    parser.add_argument("--start", required=True, help="Starting address, must be in the form of '1234 Example Street, City, State Zip Code'")
    parser.add_argument("--end", required=True, help="Destination address, must be in the form of '1234 Example Street, City, State Zip Code'")
    parser.add_argument("--method", default="DRIVE", help="Method of travel")
    parser.add_argument("--time", default="07:30", help="Normal departure time")
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        logger.info("Starting the commute notification script")

        msg = construct_commute_message(args.start, args.end, args.time, args.method)
        send_sms_message(msg, GMAIL_ADDRESS, PHONE_NUMBER)

    except Exception as e:
        logger.error("Failed to send message")
        raise e

if __name__ == "__main__":
    main()