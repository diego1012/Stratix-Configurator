from gui.panel import Panel
import traceback
from functions import log_message

test = True

if __name__ == "__main__":
    try:
        Panel(test).root.mainloop()
    except Exception as e:
        print(traceback.format_exc())
        log_message(traceback.format_exc())