# Auto configurator for Rockwell Wall Stratix devices (v1.0.0)

This tool was developed to simplify the re-configuration process of the Stratix switches in our internal lab. This is the first step in our initiative towards an automated network architecture, and consists of a compact UI that allows you to quickly upload default switch configurations.<br>

Hopefully this tool will save us time and headaches and let our team focus on the real replication and testing tasks. <br>

## Worskpace settings

v1.0.0 requires the creation of two environment variables:
- STX_USER
- STX_PWD<br>

We plan to add a functionality for custom credentials in the next release.<br>

## Creation of .exe file

If you are contributing to the app, you can use the following command in your workspace to create the .exe file:
```
<code>pyinstaller --onefile --noconsole --icon=Images/RA.ico  main.py</code>
```
