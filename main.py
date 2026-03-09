from functions import check_difference_config_backup
import tkinter as tk
from tkinter import ttk

class Panel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Configuration Backup Checker")

        self.textStatus = tk.StringVar()

        tk.Label(self.root, text="Configuration Path:").grid(row=0, column=0, padx=10, pady=10)
        opciones = self.get_options()
        self.combo = ttk.Combobox(self.root, values=opciones)
        self.combo.grid(row=0, column=1, padx=10, pady=10)
        self.combo.current(0)

        # Button for updating options
        tk.Button(self.root, text="Update Options", command=self.update_options).grid(row=0, column=2, padx=10, pady=10)

        # Button for checking differences
        tk.Button(self.root, text="Check Differences", command=self.check_differences).grid(row=1, column=0, padx=10, pady=10)

        # Button for loading configuration
        self.loadConfigBtn = tk.Button(self.root, text="Load Configuration", state="disabled")
        self.loadConfigBtn.grid(padx=10, pady=10, columnspan=3)

        # Label for displaying status messages
        self.label_message = tk.Label(self.root, textvariable=self.textStatus)
        self.label_message.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        self.label_message.config(fg="blue", relief="sunken", width=40, height=10)


    def get_options(self) -> list:
        return ["Opción A", "Opción B", "Opción C"]

    def update_options(self)-> None:
        new_options = ["Opción X", "Opción Y", "Opción Z"]
        self.combo['values'] = new_options
        self.combo.current(1)

    def check_differences(self) -> bool:
        self.textStatus.set("Checking differences...")
        self.loadConfigBtn.config(state="normal")


if __name__ == "__main__":
    #print(check_difference_config_backup(path, network))
    Panel().root.mainloop()