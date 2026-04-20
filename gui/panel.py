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
from functions.utils import get_switch_name

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

        # set initial conditions for update buttons and dropdowns
        self.frameSerial.combo.config(state="normal")
        self.frameSerial.updateOptionBtn.config(state="normal")
        self.framePath.combo.config(state="disabled")
        self.framePath.updateOptionBtn.config(state="disabled")

    def select_method(self):
        method = self.var1.get()
        if method == 1:
            self.frameSerial.combo.config(state="normal")
            self.frameSerial.updateOptionBtn.config(state="normal")
            self.framePath.combo.config(state="disabled")
            self.framePath.updateOptionBtn.config(state="disabled")
            self.update_options(serial_comms=True)
        elif method == 2:
            self.frameSerial.combo.config(state="disabled")
            self.frameSerial.updateOptionBtn.config(state="disabled")
            self.framePath.combo.config(state="normal")
            self.framePath.updateOptionBtn.config(state="normal")
            self.update_options(serial_comms=False)
        elif method == 3:
            self.frameSerial.combo.config(state="normal")

    def get_options(self, serial_comms=False) -> list:
        return generate_dropdowns(test=self.test, serial=serial_comms)

    def update_options(self, serial_comms=False)-> None:
        self.stratixInformation = self.get_options(serial_comms)
        if serial_comms == 0:
            self.framePath.combo['values'] = self.stratixInformation[0]
            try:
                self.framePath.combo.current(0)
            except tk.TclError:
                log_message(traceback.format_exc())
        else:
            self.frameSerial.combo['values'] = self.stratixInformation[0]
            if len(self.frameSerial.combo['values']) == 0: self.frameSerial.combo.set("")
            try:
                self.frameSerial.combo.current(0)
            except tk.TclError:
                log_message(traceback.format_exc())

    def check_differences(self) -> bool:
        # Disable buttons to prevent multiple clicks
        self.frameLoadConfig.disable_all()
        self.framePath.disable_all()
        self.frameSerial.disable_all()

        # Change text message
        self.frameLoadConfig.label_message.config(bg="yellow")

        if self.var1.get() == 1:
            self.frameLoadConfig.textStatus.set(f"Checking file and configuration {self.frameSerial.combo.get()} ...")
            position = self.stratixInformation[0].index(self.frameSerial.combo.get())
            device = "C:/Users/Test/Desktop/Backups/" + get_switch_name(self.frameSerial.combo.get()) + "backup"
            
        if self.var1.get() == 2:
            self.frameLoadConfig.textStatus.set(f"Checking file and configuration {self.framePath.combo.get()} ...")
            position = self.stratixInformation[0].index(self.framePath.combo.get())
            device = "C:/Users/Test/Desktop/Backups/" + self.stratixInformation[0][position] + "backup"
        print(device, position)

        # Start a new thread to check differences
        threading.Thread(target=self.check_differences_thread, args=(device, self.stratixInformation[1][position])).start()

    def check_differences_thread(self, device: str, network_device: dict):
        result = check_difference_config_backup(device, network_device)

        if 'host' in network_device.keys():
            device_name = self.framePath.combo.get()
        else:
            device_name = self.frameSerial.combo.get()
        self.frameLoadConfig.status_message(result, device_name, network_device)

    def loading_configuration_thread(self):
        if self.var1.get() == 1:
            position = self.stratixInformation[0].index(self.frameSerial.combo.get())
            switch_name = get_switch_name(self.frameSerial.combo.get())
            device = "C:/Users/Test/Desktop/Backups/" + switch_name + "backup"

        else:
            position = self.stratixInformation[0].index(self.framePath.combo.get())
            device = "C:/Users/Test/Desktop/Backups/" + self.framePath.combo.get() + "backup"
        
        network_device = self.stratixInformation[1][position]
        result = load_configuration(device, network_device)

        if self.var1.get() == 1:
            self.frameLoadConfig.status_load(result, self.frameSerial.combo.get(), network_device)
        else:
            self.frameLoadConfig.status_load(result, self.framePath.combo.get(), network_device)




