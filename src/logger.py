import logging  #Python’s built-in module for logging messages instead of printing them
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"  # Purpose → each run creates a unique log file.
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)     #os.getcwd() → gets current working directory.os.path.join() → joins paths in a cross-platform way.
os.makedirs(logs_path,exist_ok=True)   #os.makedirs(logs_path, exist_ok=True) → creates the folder path if it doesn’t exist.

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

