import tkinter as tk
from tkinter import ttk
from functions import log_message
from threading import Thread

class LoadConfigFrame(tk.LabelFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.listBacukp = []
        self.listConfig = []

        self.textStatus = tk.StringVar(value="Waiting for user action...")

        self.checkDiffBtn = tk.Button(parent, text="Load Configuration", command=controller.check_differences)
        self.checkDiffBtn.grid(row=0, column=0, padx=10, pady=10)

        self.newWindow = tk.Button(parent, text="Check Differences", command=lambda: self.open_comparation_window(parent))
        self.newWindow.grid(row=1, column=0, padx=10, pady=10)

        # Label for displaying status messages
        self.label_message = tk.Label(parent, textvariable=self.textStatus, wraplength=300)
        self.label_message.grid(row=0, column=1, columnspan=2, rowspan=2, padx=10, pady=10)
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

    def status_message(self, result: tuple, stratix: str, network_device: dict)-> None:

        self.listBacukp = result[2]
        self.listConfig = result[3]

        if result[0]:
            self.yesBtn.config(state="normal")
            self.noBtn.config(state="normal")
            self.label_message.config(bg="#27F53C")
            self.textStatus.set(f"File and configuration are the same! -> {self.controller.framePath.combo.get()}")
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

    def open_comparation_window(self, root):
        comparation = tk.Toplevel(root)
        comparation.title("Comparation Window")
        #new_window.geometry("300x200")
        comparation.grab_set()  # Make the new window modal (optional)
        
        comparation.columnconfigure(1, weight=1)
        comparation.rowconfigure(1, weight=1)

        #Add widgets directly to the new window

        self.textBackup = tk.Text(comparation)
        self.textBackup.grid( row=0, column=1)

        scrollBackup = tk.Scrollbar(comparation)
        scrollBackup.grid(row=0, column=0, sticky='ns')
        scrollBackup.config(command=self.sync_scroll)

        self.textConfig = tk.Text(comparation)
        self.textConfig.grid( row=0, column=2)

        # Define styles
        self.textBackup.tag_configure(True, background="#ff5959")
        self.textBackup.tag_configure(False, background="#ffffff")
        self.textConfig.tag_configure(True, background="#ff5959")
        self.textConfig.tag_configure(False, background="#ffffff")

        # Insert lines with alternating colors
        for i in range(self.listBacukp.__len__()):
            if i <= 9:
                space = " " * 4
            elif 10 <= i <= 99:
                space = " " * 3
            else:
                space = " " * 2

            tag = True if self.listBacukp[i] != self.listConfig[i] else False
            self.textBackup.insert("end", str(i) + space + self.listBacukp[i] + "\n", tag)
            self.textConfig.insert("end", str(i) + space + self.listConfig[i] + "\n", tag)

        self.textBackup.config(state="disabled")
        self.textConfig.config(state="disabled")

    def sync_scroll(self, *args):
    # Move both text widgets when the scrollbar is dragged
        self.textBackup.yview(*args)
        self.textConfig.yview(*args)