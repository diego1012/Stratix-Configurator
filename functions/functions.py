import os
import re

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
        username: Switch login username
        password: Switch login password

    Returns:
        A tuple containing:
            list(str): list with the names of all the Stratix devices with a backup in this folder
            list(dict): list with the netmiko object structure for each of the Stratix switches

    """

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

    backup_files = [file for file in os.listdir(source_folder) if re.fullmatch(filename_pattern, file)!=None]
    stratix_names = [name[:5] for name in backup_files]

    try: 
        if username==None and password==None:
            switch_username = os.environ['STX_USER']
            switch_password = os.environ['STX_PWD']
        else:
            switch_username = username
            switch_password = password
            
    except KeyError:
            switch_username = 'username'
            switch_password = 'password'


    netmiko_structures = [{'device_type': 'cisco_ios',
                           'host': ip_mapper[name],
                           'username': switch_username,
                           'password': switch_password} for name in stratix_names]
    
    return (stratix_names, netmiko_structures)

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
