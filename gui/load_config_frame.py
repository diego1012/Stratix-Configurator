import tkinter as tk
from tkinter import ttk
from functions import log_message
from threading import Thread

class LoadConfigFrame(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.textStatus = tk.StringVar(value="Waiting for user action...")

        self.checkDiffBtn = tk.Button(parent, text="Load Configuration", command=controller.check_differences)
        self.checkDiffBtn.grid(row=1, column=0, padx=10, pady=10)

        # Label for displaying status messages
        self.label_message = tk.Label(parent, textvariable=self.textStatus, wraplength=300)
        self.label_message.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        self.label_message.config(relief="sunken", width=40, height=10, font=("Arial", 12), bg="white")

        # Button for loading configuration
        tk.Label(parent, text="Are you sure you want to load this configuration?").grid(row=2, columnspan=3, padx=10, pady=10)

        self.yesBtn = tk.Button(parent, text="Yes", state="disabled", height=1, width=10, font=("Arial", 12), command= self.button_yes)
        self.yesBtn.grid(row=3, column=0, padx=(30,5), pady=(10, 20))

        self.noBtn = tk.Button(parent, text="No", state="disabled", height=1, width=10, font=("Arial", 12), command=self.button_no)
        self.noBtn.grid(row= 3, column=2, padx=15, pady=(10, 20))

    def disable_all(self):
        self.checkDiffBtn.config(state="disabled")
        self.yesBtn.config(state="disabled")
        self.noBtn.config(state="disabled")

    def status_message(self, result: int, stratix: str, network_device: dict)-> None:

        if result[0]:
            self.yesBtn.config(state="normal")
            self.noBtn.config(state="normal")
            self.label_message.config(bg="#27F53C")
            self.textStatus.set(f"File and configuration are the same! -> {self.combo.get()}")
        else:
            match result[1]:
                case 0:
                    self.textStatus.set(f"Backup file and configuration are different! {stratix}, if you are sure that you want to load the configuration, please click the Load Configuration button.")
                    self.label_message.config(bg="#F5C227")
                    self.yesBtn.config(state="normal")
                    self.noBtn.config(state="normal")
                case 1:
                    self.textStatus.set(f"Connection error with Stratix {stratix}! Please check the connection with {network_device['host']} or ssh configuration")
                    self.label_message.config(bg="#F53527")
                    self.controller.framePath.combo.config(state="readonly")
                    self.controller.framePath.updateOptionBtn.config(state="active")
                case 2:
                    self.textStatus.set(f"Empty backup file for {stratix}! Please check the backup file.")
                    self.label_message.config(bg="#F53527")
                    self.controller.framePath.combo.config(state="readonly")
                    self.controller.framePath.updateOptionBtn.config(state="active")
                case 3:
                    self.textStatus.set(f"Backup file does not exist for {stratix}! Please check the backup file.")
                    self.label_message.config(bg="#F53527")
                    self.controller.framePath.combo.config(state="readonly")
                    self.controller.framePath.updateOptionBtn.config(state="active")

        self.checkDiffBtn.config(state="normal")

    def button_no(self):
        self.yesBtn.config(state="disabled")
        self.noBtn.config(state="disabled")
        self.checkDiffBtn.config(state="active")
        self.controller.framePath.combo.config(state="readonly")
        self.controller.framePath.updateOptionBtn.config(state="active")
        self.textStatus.set("Waiting for user action...")
        self.label_message.config(bg='white')

    def button_yes(self):
        self.textStatus.set(f"Loading configuration {self.combo.get()} ...")
        self.label_message.config(bg="#27D3F5")
        self.yesBtn.config(state="disabled")
        self.noBtn.config(state="disabled")
        self.checkDiffBtn.config(state="disabled")
        self.controller.framePath.combo.config(state="disabled")
        self.controller.framePath.updateOptionBtn.config(state="disabled")
        Thread(target=self.controller.loading_configuration_thread).start()

    def status_load(self, result: bool, stratix: str, network_device: dict): 
        if result:
            self.textStatus.set(f"Configuration loaded successfully! {stratix}")
            self.label_message.config(bg="#27F53C")
            self.checkDiffBtn.config(state="active")
            self.controller.framePath.combo.config(state="readonly")
            self.updateOptionBtn.config(state="active")
        else:
            self.textStatus.set(f"Error loading configuration! {stratix}, please check the connection with {network_device['host']} or ssh configuration")
            self.label_message.config(bg="#F53527")
            self.checkDiffBtn.config(state="active")
            self.controller.framePath.combo.config(state="readonly")
            self.controller.framePath.updateOptionBtn.config(state="active")