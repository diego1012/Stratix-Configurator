from pathlib import Path
import os
from datetime import datetime

def log_file_verification() -> bool:

    """
    
    This function checks if the log file and its containing folder exist. 
    If they do not exist, it creates them. 
    It returns True if the verification and creation (if necessary) were successful, and False if any errors occurred during the process.
    
    Returns:
        bool: True if the log file and folder are verified or created successfully, False otherwise."""

    try:
        folder_path = Path(r"C:\Users\Public\Documents\Rockwell\Log stratix config")
        file_path = folder_path / "log.txt"

        # Check if the folder exists, if not create it. Then check if the file exists, if not create it.
        if not folder_path.exists():
            os.mkdir(folder_path)
            with open(file_path, 'w') as f:
                f.write(f"< -------------------- Log file created {datetime.now()} -------------------->\n\n")

        # If the folder exists but the file does not, create the file and write the header.
        elif not file_path.exists():
            with open(file_path, 'w') as f:
                f.write(f"<-------------------- Log file created {datetime.now()} -------------------->\n\n")

        return True

    except Exception as e:
        master_log(e)
        return False

def log_message(message: str)-> bool: 

    """
    This function takes a message as input and appends it to the log file with a timestamp. 
    It returns True if the message was successfully logged, and False if any errors occurred during the process.

    Args:
        message (str): The message to be logged.
    Returns:
        bool: True if the message was successfully logged, False otherwise.
    """

    try:
        if log_file_verification():
            folder_path = Path(r"C:\Users\Public\Documents\Rockwell\Log stratix config")
            file_path = folder_path / "log.txt"

            with open(file_path, 'a') as f:
                f.write(f"# ------ {datetime.now()} ------\n {message}\n\n")
            return True
        
        else:
            master_log(r"Log file verification failed. Message could not be logged.")
            return False

    except Exception as e:
        master_log(e)
        return False
    
def master_log(message: str):

    """
    This function takes a message as input and appends it to the master log file with a timestamp. 
    It returns True if the message was successfully logged, and False if any errors occurred during the process.

    Args:
        message (str): The message to be logged.
    """

    try:
        file_path = "master_log.txt"
        
        with open(file_path, 'a') as f:
            f.write(f"# ------ {datetime.now()} ------\n {message}\n\n")

    except Exception as e:
        print(f"An error occurred writing to master log: {e}")            