"""
This logger could have been implemented as simple print statements with the output of the python file
being piped into a log file (python3 main.py >> logs.log) but this was honestly easier
"""

import logging
from pathlib import Path

# setup the logging directory and file
BASE_DIR = Path(__file__).parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "commute_assistant.log"

# configuration the logger if it has not already been setup
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

logger = logging.getLogger(__name__)