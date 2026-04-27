import logging
import os
import re
import serial
import time

from logging import Logger
from os import path
from netmiko import ConnectHandler, file_transfer
from serial.tools.list_ports_windows import comports
from .log import log_message

BACKUPS_FILEPATH = "C:/Users/Test/Desktop/Backups"

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
    
    # Read backup file
    try:
        with open(stratix_backup, 'r', encoding='utf-8') as f:
            backup_file = f.readlines()
            if backup_file == '':
                code_error = 2
            else:
                backup_file = [s.replace("\n", "") for s in backup_file[4:]]

            backup_file = [x for x in backup_file if x != '' and x != '!' ]

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
            response_config = connect.send_command(message, read_timeout= 20).split("\n")
            response_config = response_config[6:-1]
            response_config = [x for x in response_config if x != '' and x != '!' ]
            connect.disconnect()

        except Exception as e:
            code_error = 1

    return (response_config==backup_file, code_error, backup_file, response_config)

def generate_dropdowns(logger: Logger, credentials: list = [None]*2, serial: bool = False, test: bool = False) -> tuple:

    """
    Generate the dropdown menus for the Stratix Configurator app

    Args:
        logger (Logger): Logger object that will be used to write diagnostics messages
        credentials (list): List of 2 elements containing the login credentials
        serial (bool): Flag to indicate if customer is using serial or EtherNet/IP communication
        test (bool): Flag to indicate if app is running in test mode

    Returns:
        A tuple containing:
            list: list with the names of all the Stratix devices with a backup in this folder
            list: list with the netmiko object structure for each of the Stratix switches
    """

    # Test enviorement

    if not test:
        source_folder = r"C:\Users\Test\Desktop\Backups"

    else:
        source_folder = os.getcwd() + "/Backups"

    logger = logger

    stratix_names, netmiko_structures = get_structures(logger, source_folder, credentials, serial)
    
    return stratix_names, netmiko_structures

def get_structures(logger:Logger, backups_folder: str, credentials: list, serial_comms: bool) -> tuple:

    """
    Generate the netmiko structure for a given switch
    Args:
        logger (Logger): Logger object that will be used to write diagnostics messages
        backups_folder (str): Full path to the folder containing the backup config files
        credentials (list): List of 2 elements containing the login credentials
        serial (bool): Flag to indicate if customer is using serial or EtherNet/IP communication

    Returns:
        A tuple containing:
            list: list with the names of all the Stratix devices with a backup in this folder
            list: list with the netmiko object structure for each of the Stratix switches
    """
    
    ip_mapper = {
        "STX01": "192.168.3.213",
        #"STX04": "192.168.3.215",
        "STX05": "192.168.3.209",
        "STX06": "192.168.3.210",
        "STX07": "192.168.3.211",
        "STX08": "192.168.3.212",
        "STX12": "192.168.3.206",
        "STX13": "192.168.3.207",
        "STX14": "179.254.0.1",
    }

    filename_pattern = re.compile(r'STX\d{2}(-ASA|)backup')

    credentials_to_use = set_credentials(logger, credentials)

    netmiko_structures = []

    if serial_comms == 0:
        # Create list to store names of available switches
        switch_names = []

        # Build names and netmiko structures for SSH comms
        try:
            logger.info(f"Looking for backup files in {backups_folder}...")
            backup_files = [file for file in os.listdir(backups_folder) if re.fullmatch(filename_pattern, file)!=None]
            logger.info(f"Found {len(backup_files)} valid files")
            backups_folder_switch_names = [name[:5] for name in backup_files]
    
        except FileNotFoundError:
            logger.error(f"Folder {backups_folder} does not exist")

        for name in backups_folder_switch_names:
            if name in ip_mapper.keys():
                switch_structure = {
                                    'device_type': 'cisco_ios',
                                    'host': ip_mapper[name],
                                    'username': credentials_to_use[0],
                                    'password': credentials_to_use[1]
                                }
                switch_names.append(name)
                netmiko_structures.append(switch_structure)
            else:
                logger.error(f"The Stratix switch associated to file {name}backup is not accessible or does not exist")

    else:
        switch_names = []

        # Build netmiko structures for serial comms
        serial_ports = comports()
        for port in serial_ports:
            logger.info(f"Checking {port.description}")
            try:
                # Configure serial connection (standard Cisco settings)
                serial_connection = serial.Serial(
                    port=port.device,
                    baudrate=9600,
                    parity='N',
                    stopbits=1,
                    bytesize=8,
                    timeout=2 # Short timeout
                )
                
                # Send an enter to trigger a response
                serial_connection.write(b'\r\n')
                time.sleep(1)
                
                # Read response
                response = serial_connection.read(serial_connection.in_waiting).decode('utf-8', errors='ignore')
                
                # Check if it looks like a Cisco prompt
                if '>' in response or '#' in response or 'User Access' in response or 'Username' in response:
                    logger.info(f"Possible Cisco device found on {port.device}")
                    serial_connection.close()

                    #Create netmiko structure
                    cisco_serial = {
                        "device_type": "cisco_ios_serial",
                        "username": os.environ["STX_USER"],   # Customize later to allow custom credentials
                        "password": os.environ["STX_PWD"],   # Customize later to allow custom credentials
                        "fast_cli": False,
                        "serial_settings": {
                            "port": port.device,
                            "baudrate": 9600,
                            "bytesize": serial.EIGHTBITS,
                            "parity": serial.PARITY_NONE,
                            "stopbits": serial.STOPBITS_ONE,
                        },
                    }

                    netmiko_structures.append(cisco_serial)
                    switch_names.append(port.device)

                else:
                    logger.info("No Cisco switch detected.")
                serial_connection.close()
                
            except Exception as e:
                # Port might be in use or unauthorized
                logger.error(e)
                continue            

    return switch_names, netmiko_structures

def create_logger(test: bool = False) -> Logger:
    """
    Generate user-readable logger for app monitoring

    Args:
        filepath (str): Path of logs file 

    Returns:
        A tuple containing:
            logger: Logger object
    """
    if not test:
        filepath = "C:/Users/Test/Desktop/Backups/Logs/logs.txt"
    
    else:
        filepath = os.getcwd() + '/logs.txt'

    # Test enviorenment 

    if not test:
        filepath = "C:/Users/Test/Desktop/Backups/Logs/logs.txt"
    
    else:
        filepath = os.getcwd() + '/logs.txt'

    new_logger = logging.getLogger('stratix_app_logger')

    try:
        log_handler = logging.FileHandler(filepath)
    except FileNotFoundError:
        os.makedirs(filepath.split("/logs.txt")[0], exist_ok=True)
        with open('logs.txt', 'w') as log_file:
            pass
        log_handler = logging.FileHandler(filepath)
    except Exception as e:
        with open(os.getcwd() + '/logs.txt', 'w') as log_file:
            pass
        log_handler = logging.FileHandler(filepath)

    log_handler.setLevel(logging.DEBUG) # Log all debug messages and higher to file
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    new_logger.addHandler(log_handler)
    new_logger.setLevel(logging.DEBUG)
    new_logger.propagate = False

    return new_logger

def set_credentials(logger: Logger, credentials: list) -> tuple[str,str]:
    """
    Sets credentials to be used for switch log in

    Args:
        logger (Logger): logs events inside this function
        credentials [str,str]: list of 2 string containing username and password

    Returns:
        A tuple containing:
            switch_username (str)
            switch_password (str)
    """

    try: 
        if len(credentials)==2 and credentials == [None]*2:
            switch_username = os.environ['STX_USER']
            switch_password = os.environ['STX_PWD']
        else:
            logger.info("Custom credentials provided by user")
            switch_username = credentials[0]
            switch_password = credentials[1]
            
    except KeyError:
        logger.warning(f"Local environment variables STX_USER and STX_PWD for Rockwell credentials missing! Generating generic credentials...")
        logger.info("It is recommended to create these environment variables to avoid entering credentials in each new session")
        switch_username = 'username'
        switch_password = 'password'

    return (switch_username, switch_password)

def load_configuration(stratix_file: str, network_device: dict) -> bool:
    """
    Sets credentials to be used for switch log in

    Args:
        logger (Logger): logs events inside this function
        credentials (list): list of 2 string containing username and password

    Returns:
        A tuple containing:
            str: username
            str: password
    """

    try:
        connect = ConnectHandler(**network_device)
        connect.enable()

        if network_device["device_type"] == "cisco_ios_serial":
            switch_hostname = connect.send_command("show running-config | include hostname")
            switch_name = switch_hostname.split(" ")[1]
            stratix_file = path.join(BACKUPS_FILEPATH, f"{switch_name}backup")

        # command = connect.send_config_from_file(config_file=stratix_file)

        results = file_transfer(connect, 
                                source_file=stratix_file,
                                dest_file=f"{switch_name}backup.txt",
                                file_system="flash",
                                direction="put",
                                overwrite_file=True
                               )
        print(results) # delete after tr

        command = connect.send_command(f"configure replace flash:{switch_name}backup.txt")
        command = connect.send_command("copy running-config startup-config")

        connect.disconnect()
        return True
    
    except Exception as e:
        log_message(f"An error occurred while loading the configuration: {e}")
        return False
    
def get_switch_name(serial_port_name: str) -> str: #update this function to use the credentials entered by customer. These credentials should be an argument of this function
    """
    Retrieves the hostname of a switch connected through its console port

    Args:
        serial_port_name (str): name of the serial port connected to the switch

    Returns:
        str: name of the switch
    """

    cisco_serial = {
                        "device_type": "cisco_ios_serial",
                        "username": os.environ["STX_USER"],
                        "password": os.environ["STX_PWD"],
                        "fast_cli": False,
                        "serial_settings": {
                            "port": serial_port_name,
                            "baudrate": 9600,
                            "bytesize": serial.EIGHTBITS,
                            "parity": serial.PARITY_NONE,
                            "stopbits": serial.STOPBITS_ONE,
                        },
                    }
    
    connection = ConnectHandler(**cisco_serial)
    switch_hostname = connection.send_command("show running-config | include hostname")
    switch_name = switch_hostname.split(" ")[1]

    return switch_name

def list_serial_ports() -> list:
    """
    Returns a list with the active serial ports in the PC

    Returns:
        list: list of active serial ports
    """

    ports = comports()
    return ports
