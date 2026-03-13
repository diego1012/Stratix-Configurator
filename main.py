from gui.panel import Panel
from functions import log_message

if __name__ == "__main__":
    try:
        Panel().root.mainloop()
    except Exception as e:
        log_message(f"An error occurred while running the application: {e}")
        print(e)