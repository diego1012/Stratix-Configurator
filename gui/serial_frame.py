import tkinter as tk
from tkinter import ttk
from functions import log_message
import traceback

class SerialFrame(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(parent, relief= 'flat', text="Serial Port:").grid(row=0, column=0, padx=20, pady=10)

        self.combo = ttk.Combobox(parent, values=['COM1', 'COM2', 'COM3'], state="readonly", justify="center", width=15)
        self.combo.grid(row=0, column=1, padx=20, pady=10)
        self.combo.option_add('*TCombobox*Listbox.Justify', 'center') 

        self.updateOptionBtn = tk.Button(parent, image=controller.pixel_art, command=self.update_ports)
        self.updateOptionBtn.grid(row=0, column=2, padx=20, pady=10, ipadx=10)

    def update_ports(self):
        pass