import logging
import os
import re

from logging import Logger
from os import path
from netmiko import ConnectHandler
from functions.log import log_message

def check_difference_config_backup(stratix_backup: str, network_device:dict) -> tuple:
    
    """
    Check the difference between the stratix backup file and the current stratix configuration

    Args:
        stratix backup (str): Backup file name.
        network_device (int): This argument must have the next structure {"host": <ip_address>, "username": "Admin", "password": "Rockwell123", "device_type": "cisco_ios"}.

    Returns:
        A tuple containing:
            bool: the current configuration and backup configuration are the same.
            int: error code

    Error code:
        0: Function executed correctly
        1: Connection error with Stratix
        2: Empty file
        3: Backup file not exist
    """

    backup_file = "+"
    response_config = "-"
    code_error = 0

    print(stratix_backup)
    
    # Read backup file
    try:
        with open(stratix_backup, 'r', encoding='utf-8') as f:
            backup_file = f.readlines()
            if backup_file == '':
                code_error = 2
            else:
                backup_file = "".join(backup_file[4:])
    except FileNotFoundError:
        code_error = 3

    # if there is an error code, it's not neccesary to continue with stratix connection
    if code_error == 0:

        try:
            # Stratix connection
            connect = ConnectHandler(**network_device)
            connect.enable()

            # Read current config stratix
            message = 'show run'    
            response_config = connect.send_command(message).split("\n")
            response_config = "\n".join(response_config[6:])
            connect.disconnect()

        except Exception as e:
            code_error = 1

    return (response_config==backup_file, code_error)

def generate_dropdowns(source_folder=r"C:\Users\Test\Desktop\Backups", username=None, password=None) -> tuple:

    """
    Generate the dropdown menus for the Stratix Configurator app

    Args:
        source folder (str): The absolute path to the folder where backup config files are located
        username (str): Switch login username
        password (str): Switch login password

    Returns:
        A tuple containing:
            list(str): list with the names of all the Stratix devices with a backup in this folder
            list(dict): list with the netmiko object structure for each of the Stratix switches
    """

    logger = create_logger()

    ip_mapper = {
        "STX02": "192.168.3.213",
        "STX04": "192.168.3.215",
        "STX05": "192.168.3.209",
        "STX06": "192.168.3.210",
        "STX07": "192.168.3.211",
        "STX08": "192.168.3.212",
        "STX12": "192.168.3.206",
        "STX13": "192.168.3.207",
        "STX14": "179.254.0.1",
    }

    filename_pattern = re.compile(r'STX\d{2}(-ASA|)backup')

    try:
        logger.info(f"Looking for backup files in {source_folder}...")
        backup_files = [file for file in os.listdir(source_folder) if re.fullmatch(filename_pattern, file)!=None]
        logger.info(f"Found {len(backup_files)} valid files")
        stratix_names = [name[:5] for name in backup_files]
    
    except FileNotFoundError:
         logger.error(f"Folder {source_folder} does not exist")

    credentials = set_credentials(logger, username, password)

    netmiko_structures = []

    for name in stratix_names:
        if name in ip_mapper.keys():
            switch_structure = {
                                'device_type': 'cisco_ios',
                                'host': ip_mapper[name],
                                'username': credentials[0],
                                'password': credentials[1]
                               }
            netmiko_structures.append(switch_structure)
        else:
            logger.error(f"The Stratix switch associated to file {name}backup is not accessible or does not exist")
            stratix_names.remove(name)
    
    return stratix_names, netmiko_structures

def create_logger(filepath="C:/Users/Test/Desktop/Backups/Logs/logs.txt") -> Logger:
    """
    Generate logger for app monitoring

    Args:
        filepath (str): Path of logs file 

    Returns:
        A tuple containing:
            logger (Logger): Logger object
    """

    new_logger = logging.getLogger('stratix_app_logger')

    try:
        log_handler = logging.FileHandler(filepath)
    except FileNotFoundError:
        os.makedirs(filepath.split("/logs.txt")[0], exist_ok=True)
        with open('logs.txt', 'w') as log_file:
            pass
        log_handler = logging.FileHandler(filepath)

    log_handler.setLevel(logging.DEBUG) # Log all debug messages and higher to file
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    new_logger.addHandler(log_handler)
    new_logger.setLevel(logging.DEBUG)

    return new_logger

def set_credentials(logger: Logger, username=None, password=None) -> tuple:
    """
    Sets credentials to be used for switch log in

    Args:
        logger (Logger): logs events inside this function
        username (str)
        password (str)

    Returns:
        A tuple containing:
            switch_username (str)
            switch_password (str)
    """

    try: 
        if username==None and password==None:
            switch_username = os.environ['STX_USER']
            switch_password = os.environ['STX_PWD']
        else:
            logger.info("Custom credentials provided by user")
            switch_username = username
            switch_password = password
            
    except KeyError:
        logger.warning(f"Local environment variables STX_USER and STX_PWD for Rockwell credentials missing! Generating generic credentials...")
        logger.info("It is recommended to create these environment variables to avoid entering credentials in each new session")
        switch_username = 'username'
        switch_password = 'password'

    return (switch_username, switch_password)

def load_configuration(stratix_file: str, network_device: dict) -> bool:

    try:
        connect = ConnectHandler(**network_device)
        connect.enable()

        command = connect.send_config_from_file(config_file=stratix_file)
        
        connect.disconnect()
        return True
    
    except Exception as e:
        log_message(f"An error occurred while loading the configuration: {e}")
        return False
