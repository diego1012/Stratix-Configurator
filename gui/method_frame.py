import tkinter as tk
from tkinter import ttk
from functions import log_message

class MethodFrame(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.rb1 = tk.Radiobutton(parent, text="Serial", variable=controller.var1, value="1", command=controller.select_method)
        self.rb1.grid(row=0, column=0, padx=10, pady=10)
        self.rb2 = tk.Radiobutton(parent, text="SSH", variable=controller.var1, value="2", command=controller.select_method)
        self.rb2.grid(row=0, column=1, padx=10, pady=10)
