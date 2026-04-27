import traceback
from functions import log_message
from GUI_Flet import GUI
import flet as ft


test = False

if __name__ == "__main__":
    try:
        ft.run(main=GUI)  # Start the Flet app
        #Panel(test).root.mainloop()
    except Exception as e:
        print(traceback.format_exc())
        log_message(traceback.format_exc())