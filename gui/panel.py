from functions.utils import check_difference_config_backup, generate_dropdowns, load_configuration
import tkinter as tk
from tkinter import ttk
import threading
import traceback
from functions import log_message
from gui.config_frame import ConfigFrame
from gui.method_frame import MethodFrame
from gui.serial_frame import SerialFrame
from gui.load_config_frame import LoadConfigFrame

class Panel:
    def __init__(self, test: bool):
        self.root = tk.Tk()
        self.root.title("Configuration Backup Checker")

        try:
            self.root.iconbitmap('Images/RA.ico')
        except:
            pass

        # Varible for test
        self.test = test


        self.pixel_art = tk.PhotoImage(file="Images/actualizar.png")
        self.stratixInformation = self.get_options()

        # Frame for configuration path

        containerPath = tk.LabelFrame(self.root, text="Configuration Path", padx=20, pady=5)
        containerPath.pack(padx=20, pady=5, fill="x")
        
        self.framePath = ConfigFrame(containerPath, self)

        # Frame for method selection

        self.var1 = tk.IntVar(value=1)

        containerMethod = tk.LabelFrame(self.root, text="Method Selection", padx=20, pady=5)
        containerMethod.pack(padx=20, pady=5, fill="both")

        self.frameMethod = MethodFrame(containerMethod, self)

        # Frame for  serial communication

        containerSerial = tk.LabelFrame(self.root, text="Serial Communication", padx=20, pady=5)
        containerSerial.pack(padx=20, pady=5, fill="both")

        self.frameSerial = SerialFrame(containerSerial, self)

        # Frame for load configuration

        containerLoadConfig = tk.LabelFrame(self.root, text="Load Configuration", padx=20, pady=5)
        containerLoadConfig.pack(padx=20, pady=5, fill="both")
        
        self.frameLoadConfig = LoadConfigFrame(containerLoadConfig, self)

    def select_method(self):
        method = self.var1.get()
        if method == 1:
            self.frameSerial.combo.config(state="normal")
        elif method == 2:
            self.frameSerial.combo.config(state="disabled")
        elif method == 3:
            self.frameSerial.combo.config(state="normal")

    def get_options(self) -> list:
        return generate_dropdowns(test=self.test)    

    def update_options(self)-> None:
        self.stratixInformation = self.get_options()
        self.framePath.combo['values'] = self.stratixInformation[0]
        try:
            self.framePath.combo.current(0)
        except tk.TclError:
            log_message(traceback.format_exc())

    def check_differences(self) -> bool:

        # Disable buttons to prevent multiple clicks
        self.frameLoadConfig.disable_all()
        self.framePath.disable_all()

        # Change text message

        self.frameLoadConfig.label_message.config(bg="yellow")
        self.frameLoadConfig.textStatus.set(f"Checking file and configuration {self.framePath.combo.get()} ...")
        position = self.stratixInformation[0].index(self.framePath.combo.get())
        device = "C:/Users/Test/Desktop/Backups/" + self.stratixInformation[0][position] + "backup"

        # Start a new thread to check differences
        threading.Thread(target=self.check_differences_thread, args=(device, self.stratixInformation[1][position])).start()

    def check_differences_thread(self, device, network_device):
        result = check_difference_config_backup(device, network_device)
        self.frameLoadConfig.status_message(result, self.framePath.combo.get(), network_device)

    def loading_configuration_thread(self):
        position = self.stratixInformation[0].index(self.combo.get())
        device = "C:/Users/Test/Desktop/Backups/" + self.stratixInformation[0][position] + "backup"
        network_device = self.stratixInformation[1][position]
        result = load_configuration(device, network_device)
        self.frameLoadConfig.status_load(result, self.framePath.combo.get(), network_device)




