import tkinter as tk
from tkinter import ttk
from functions import log_message
from functions.utils import list_serial_ports
import traceback

class SerialFrame(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(parent, relief= 'flat', text="Serial Port:").grid(row=0, column=0, padx=20, pady=10)

        self.combo = ttk.Combobox(parent, values=[], state="readonly", justify="center", width=15)
        self.combo.grid(row=0, column=1, padx=20, pady=10)
        self.combo.option_add('*TCombobox*Listbox.Justify', 'center') 

        self.updateOptionBtn = tk.Button(parent, image=controller.pixel_art, command= lambda:controller.update_options(serial_comms=True))
        self.updateOptionBtn.grid(row=0, column=2, padx=20, pady=10, ipadx=10)

    def disable_all(self):
        self.combo.config(state="disabled")
        self.updateOptionBtn.config(state="disabled")

    # def update_ports(self):
    #     self.combo['values'] = 