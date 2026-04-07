import tkinter as tk
from tkinter import ttk
from functions import log_message
import traceback

class ConfigFrame(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(parent, relief= 'flat', text="Configuration Path:").grid(row=0, column=0, padx=10, pady=10)
        controller.stratixInformation = controller.get_options()
        self.combo = ttk.Combobox(parent, values=controller.stratixInformation[0], state="readonly", justify="center", width=30)
        self.combo.grid(row=0, column=1, padx=10, pady=10)
        try:
            self.combo.current(0)
        except tk.TclError:
            log_message(traceback.format_exc())

        self.combo.option_add('*TCombobox*Listbox.Justify', 'center') 

        # Button for updating options
        self.updateOptionBtn = tk.Button(parent, image=controller.pixel_art, command=controller.update_options)
        self.updateOptionBtn.grid(row=0, column=2, padx=10, pady=10, ipadx=10)

    def disable_all(self):
        self.combo.config(state="disabled")
        self.updateOptionBtn.config(state="disabled")