"""
Main script for the project. I could actually add a shebang at the top of this file that would let me run it
in the cronjob without declaring the python interpreter, but I like to keep it explicit. 
"""
from argparse import ArgumentParser

from notifier.commute import get_commute_information
from notifier.logger import logger
from config import HOME_ADDRESS, WORK_ADDRESS, PHONE_NUMBER

def parse_args():
    pass

if __name__ == "__main__":
    pass