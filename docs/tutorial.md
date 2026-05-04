## Tutorial
The app allows you to restore a backup configuration to any of the Communications Wall switches through Ethernet (SSH) or serial.

Currently, it works for one switch at a time. Synchronous configuration of multiple switches is planned for a future release.

Usage steps are straighforward:
1. Choose the communication method that you will use (SSH or serial).
2. Choose the switch you will restore the backup file to.<br>
For Ethernet comms, there is a list of available switches you can choose from.<br> 
For serial comms, you can choose from a list of available serial ports. The app <u>will only list the serial ports that are connected to a Cisco device</u>.
3. Click on _Load Configuration_. The app will compare the backup file with the current switch configuration, and identify any differences.
4. If required, you can check the differences between both configurations by clicking on _Check differences_.
5. Finally, click on _Load configuration_ if you decide to load the backup file in the switch. This step will reboot the switch so it can start running with the new configuration.

