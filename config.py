"""
File to load in environment variables from a .env file
More modular than just importing them all in main.py
"""
from dotenv import load_dotenv
import os

load_dotenv()

# attempt to hard index the variables so that if one is not found it will throw an error
try:
    GMAIL_ADDRESS = os.environ["GMAIL_ADDRESS"]
    GOOGLE_APP_PASSWORD = os.environ["GOOGLE_APP_PASSWORD"]
    PHONE_NUMBER = os.environ["PHONE_NUMBER"]
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
    HOME_ADDRESS = os.environ["HOME_ADDRESS"]
    WORK_ADDRESS = os.environ["WORK_ADDRESS"]
except KeyError:
    print("Failed to load one or more environment variables. Check to make sure you have a .env file with all necessary variables")
    raise