from functions.utils import check_difference_config_backup, generate_dropdowns, load_configuration
import tkinter as tk
from tkinter import ttk
import threading
import traceback
from functions import log_message


class Panel:
    def __init__(self, test: bool):
        self.root = tk.Tk()
        self.root.title("Configuration Backup Checker")

        try:
            self.root.iconbitmap('Images/RA.ico')
        except:
            pass

        # Variable for test
        self.test = test

        self.textStatus = tk.StringVar(value="Waiting for user action...")

        tk.Label(self.root, text="Configuration Path:").grid(row=0, column=0, padx=10, pady=10)
        self.stratixInformation = self.get_options()
        self.combo = ttk.Combobox(self.root, values=self.stratixInformation[0], state="readonly", justify="center", width=30)
        self.combo.grid(row=0, column=1, padx=10, pady=10)
        try:
            self.combo.current(0)
        except tk.TclError:
            log_message(traceback.format_exc())

        self.combo.option_add('*TCombobox*Listbox.Justify', 'center') 

        # Button for updating options
        self.updateOptionBtn = tk.Button(self.root, text="Update Options", command=self.update_options)
        self.updateOptionBtn.grid(row=0, column=2, padx=10, pady=10)

        # Button for checking differences
        self.checkDiffBtn = tk.Button(self.root, text="Load Configuration", command=self.check_differences)
        self.checkDiffBtn.grid(row=1, column=0, padx=10, pady=10)

        # Label for displaying status messages
        self.label_message = tk.Label(self.root, textvariable=self.textStatus, wraplength=300)
        self.label_message.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        self.label_message.config(relief="sunken", width=40, height=10, font=("Arial", 12), bg="white")

        # Button for loading configuration
        tk.Label(self.root, text="Are you sure you want to load this configuration?").grid(row=2, columnspan=3, padx=10, pady=10)

        self.yesBtn = tk.Button(self.root, text="Yes", state="disabled", height=1, width=10, font=("Arial", 12), command=self.button_yes)
        self.yesBtn.grid(row=3, column=0, padx=(30,5), pady=(10, 20))

        self.noBtn = tk.Button(self.root, text="No", state="disabled", height=1, width=10, font=("Arial", 12), command=self.button_no)
        self.noBtn.grid(row= 3, column=2, padx=15, pady=(10, 20))


    def get_options(self) -> list:
        return generate_dropdowns(test=self.test)    

    def update_options(self)-> None:
        self.stratixInformation = self.get_options()
        self.combo['values'] = self.stratixInformation[0]
        try:
            self.combo.current(0)
        except tk.TclError:
            log_message(traceback.format_exc())

    def check_differences(self) -> bool:

        # Disable buttons to prevent multiple clicks
        self.yesBtn.config(state="disabled")
        self.noBtn.config(state="disabled")
        self.checkDiffBtn.config(state="disabled")
        self.combo.config(state="disabled")
        self.updateOptionBtn.config(state="disabled")

        # Change text message
        self.label_message.config(bg="yellow")
        self.textStatus.set(f"Checking file and configuration {self.combo.get()} ...")
        position = self.stratixInformation[0].index(self.combo.get())
        device = "C:/Users/Test/Desktop/Backups/" + self.stratixInformation[0][position] + "backup"

        # Start a new thread to check differences
        threading.Thread(target=self.check_differences_thread, args=(device, self.stratixInformation[1][position])).start()

    def check_differences_thread(self, device, network_device):
        result = check_difference_config_backup(device, network_device)
        if result[0]:
            self.yesBtn.config(state="normal")
            self.noBtn.config(state="normal")
            self.label_message.config(bg="#27F53C")
            self.textStatus.set(f"File and configuration are the same! -> {self.combo.get()}")
        else:
            match result[1]:
                case 0:
                    self.textStatus.set(f"Backup file and configuration are different! {self.combo.get()}, if you are sure that you want to load the configuration, please click the Load Configuration button.")
                    self.label_message.config(bg="#F5C227")
                    self.yesBtn.config(state="normal")
                    self.noBtn.config(state="normal")
                case 1:
                    self.textStatus.set(f"Connection error with Stratix {self.combo.get()}! Please check the connection with {network_device['host']} or ssh configuration")
                    self.label_message.config(bg="#F53527")
                    self.combo.config(state="readonly")
                    self.updateOptionBtn.config(state="active")
                case 2:
                    self.textStatus.set(f"Empty backup file for {self.combo.get()}! Please check the backup file.")
                    self.label_message.config(bg="#F53527")
                    self.combo.config(state="readonly")
                    self.updateOptionBtn.config(state="active")
                case 3:
                    self.textStatus.set(f"Backup file does not exist for {self.combo.get()}! Please check the backup file.")
                    self.label_message.config(bg="#F53527")
                    self.combo.config(state="readonly")
                    self.updateOptionBtn.config(state="active")

        self.checkDiffBtn.config(state="normal")

    def loading_configuration_thread(self):
        position = self.stratixInformation[0].index(self.combo.get())
        device = "C:/Users/Test/Desktop/Backups/" + self.stratixInformation[0][position] + "backup"
        network_device = self.stratixInformation[1][position]
        result = load_configuration(device, network_device)

        if result:
            self.textStatus.set(f"Configuration loaded successfully! {self.combo.get()}")
            self.label_message.config(bg="#27F53C")
            self.checkDiffBtn.config(state="active")
            self.combo.config(state="readonly")
            self.updateOptionBtn.config(state="active")
        else:
            self.textStatus.set(f"Error loading configuration! {self.combo.get()}, please check the connection with {network_device['host']} or ssh configuration")
            self.label_message.config(bg="#F53527")
            self.checkDiffBtn.config(state="active")
            self.combo.config(state="readonly")
            self.updateOptionBtn.config(state="active")

    def button_no(self):
        self.yesBtn.config(state="disabled")
        self.noBtn.config(state="disabled")
        self.checkDiffBtn.config(state="active")
        self.combo.config(state="readonly")
        self.updateOptionBtn.config(state="active")
        self.textStatus.set("Waiting for user action...")
        self.label_message.config(bg='white')

    def button_yes(self):
        self.textStatus.set(f"Loading configuration {self.combo.get()} ...")
        self.label_message.config(bg="#27D3F5")
        self.yesBtn.config(state="disabled")
        self.noBtn.config(state="disabled")
        self.checkDiffBtn.config(state="disabled")
        self.combo.config(state="disabled")
        self.updateOptionBtn.config(state="disabled")
        threading.Thread(target=self.loading_configuration_thread).start()
