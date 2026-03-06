from netmiko import ConnectHandler

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

        except Exception as e:
            code_error = 1

    return (response_config==backup_file, code_error)