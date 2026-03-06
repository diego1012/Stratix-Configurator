from functions import check_difference_config_backup

network = {"host": "192.168.3.210", "username": "Admin", "password": "Rockwell123", "device_type": "cisco_ios"}
path = 'STX09backup'

print(check_difference_config_backup(path, network))