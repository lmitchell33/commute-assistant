"""
Main script for the project. I could add a shebang at the top of this file that would let me run it
in the cronjob without declaring the python interpreter, but I like to keep it explicit. 
"""
from argparse import ArgumentParser

from notifier.commute import get_commute_information
from notifier.message import send_sms_message
from notifier.logger import logger
from config import HOME_ADDRESS, WORK_ADDRESS, PHONE_NUMBER, GMAIL_ADDRESS

def construct_commute_message(start_addr, end_addr, departure_time):
    """
    Construct the SMS message to send to the user

    :param start_addr: The starting address for the commute
    :param end_addr: The ending address for the commute
    :param departure_time: Optional departure time, defaults to 7:30 AM today. Inputs can be:
    :return: The final SMS message
    """
    travel_time , directions = get_commute_information(start_addr, end_addr, departure_time)
    
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
    parser = ArgumentParser(description="Send commute information via SMS")
    parser.add_argument("--start", default=HOME_ADDRESS, help="Starting address")
    parser.add_argument("--end", default=WORK_ADDRESS, help="Destination address")
    parser.add_argument("--time", default="06:00", help="Normal departure time")
    parser.add_argument("--phone", default=PHONE_NUMBER, help="Phone number to send the message to")
    parser.add_argument("--sender", default=GMAIL_ADDRESS, help="Gmail address to send the message from")
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        logger.info("Starting the commute notification script")

        msg = construct_commute_message(args.start, args.end, args.time)
        send_sms_message(msg, args.sender, args.phone)

    except Exception as e:
        logger.error("Failed to send message")
        raise e

if __name__ == "__main__":
    main()