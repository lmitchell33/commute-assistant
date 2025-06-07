"""
File to load in environment variables from a .env file
More modular than just importing them all in main.py
"""
from dotenv import load_dotenv
import os

load_dotenv()

# Not-required environment variables
GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER") 
HOME_ADDRESS = os.environ.get("HOME_ADDRESS")
WORK_ADDRESS = os.environ.get("WORK_ADDRESS")

# attempt to hard index the variables so that if one is not found it will throw an error
try:
    GOOGLE_APP_PASSWORD = os.environ["GOOGLE_APP_PASSWORD"]
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
except KeyError:
    print("Failed to the Google App password or Google API key. Check to make sure you have a .env file with all necessary variables")
    raise