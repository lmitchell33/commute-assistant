"""
File to load in environment variables from a .env file
More modular than just importing them all in main.py
"""
from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_ADDRESS=os.environ.get("GMAIL_ADDRESS", "")
GOOGLE_APP_PASSWORD=os.environ.get("GOOGLE_APP_PASSWORD", "")
PHONE_NUMBER=os.environ.get("PHONE_NUMBER", "")
GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY", "")
HOME_ADDRESS=os.environ.get("HOME_ADDRESS", "")
WORK_ADDRESS=os.environ.get("WORK_ADDRESS", "")

# TODO: Functionality for checking to ensure the variables are set/loaded properly