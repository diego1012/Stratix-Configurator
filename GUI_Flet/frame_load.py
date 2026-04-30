import flet as ft
from functions import check_difference_config_backup, load_configuration, get_switch_name, checking_communication
from time import sleep
from threading import Thread

class FrameLoad():

    def __init__(self, parent):

        self.parent = parent

        self.modal_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete all those files?"),
            actions=[
                ft.TextButton("Yes", on_click=lambda e: parent.page.pop_dialog()),
                ft.TextButton("No", on_click=lambda e: parent.page.pop_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Modal dialog dismissed!"))
    

        self.button_check = ft.Button(
                                        content="Check Communication",
                                        icon=ft.Icons.CONNECTING_AIRPORTS,
                                        style=ft.ButtonStyle(
                                                text_style={ft.ControlState.DEFAULT: ft.TextStyle(size=12, weight=ft.FontWeight.BOLD),
                                                            ft.ControlState.DISABLED: ft.TextStyle(size=12)},
                                                padding=ft.padding.symmetric(vertical=3, horizontal=20),
                                                color={ft.ControlState.DEFAULT: ft.Colors.AMBER_400,
                                                        ft.ControlState.DISABLED: ft.Colors.WHITE_70},
                                                bgcolor={ft.ControlState.DISABLED: ft.Colors.GREY_900},
                                                side= {ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.WHITE_60),
                                                    ft.ControlState.DISABLED: ft.BorderSide(1, ft.Colors.TRANSPARENT)},
                                                icon_color={ft.ControlState.DEFAULT: ft.Colors.AMBER_400,
                                                            ft.ControlState.DISABLED: ft.Colors.WHITE_70}
                                                ),
                                        width=200,
                                        disabled=True,
                                        on_click=self.handle_check_communication,
                                        )
        
        self.button_compare = ft.Button(
                                        content="Compare Configuration",
                                        icon=ft.Icons.COMPARE_ARROWS_ROUNDED,
                                        style=ft.ButtonStyle(
                                                text_style={ft.ControlState.DEFAULT: ft.TextStyle(size=12, weight=ft.FontWeight.BOLD),
                                                            ft.ControlState.DISABLED: ft.TextStyle(size=12)}, 
                                                padding=ft.padding.only(top=3, bottom=3),
                                                color={ft.ControlState.DEFAULT: ft.Colors.BLUE_400,
                                                        ft.ControlState.DISABLED: ft.Colors.WHITE_70},
                                                bgcolor={ft.ControlState.DISABLED: ft.Colors.GREY_900},
                                                side= {ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.WHITE_60),
                                                    ft.ControlState.DISABLED: ft.BorderSide(1, ft.Colors.TRANSPARENT)},
                                                icon_color={ft.ControlState.DEFAULT: ft.Colors.BLUE_400,
                                                            ft.ControlState.DISABLED: ft.Colors.WHITE_70}
                                                ),
                                        width=200,
                                        disabled=True,
                                        on_click=self.parent.show_next_page)

        self.button_load = ft.Button(
                                        content="Load Backup",
                                        icon=ft.Icons.DOWNLOAD,
                                        style=ft.ButtonStyle(
                                            text_style={ft.ControlState.DEFAULT: ft.TextStyle(size=12, weight=ft.FontWeight.BOLD),
                                                        ft.ControlState.DISABLED: ft.TextStyle(size=12)},  
                                            padding=ft.padding.only(top=3, bottom=3),
                                            color={ft.ControlState.DEFAULT: ft.Colors.GREEN_400,
                                                    ft.ControlState.DISABLED: ft.Colors.WHITE_70},
                                            bgcolor={ft.ControlState.DISABLED: ft.Colors.GREY_900},
                                            side= {ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.WHITE_60),
                                                   ft.ControlState.DISABLED: ft.BorderSide(1, ft.Colors.TRANSPARENT)},
                                            icon_color={ft.ControlState.DEFAULT: ft.Colors.GREEN_400,
                                                        ft.ControlState.DISABLED: ft.Colors.WHITE_70}
                                            ),
                                        width=200,
                                        disabled=True,
                                        on_click= lambda e: self.handle_load_configuration(),
                                        )
        
        self.text_status = ft.Text("Waiting for user action...", color=ft.Colors.BLACK, size=12, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

        self.container_status = ft.Container(
                                        alignment=ft.Alignment.CENTER,
                                        height=200, width=200,
                                        bgcolor=ft.Colors.WHITE,
                                        border_radius=5,
                                        content=self.text_status,
                                        padding= ft.padding.all(20),
                                    )

        self.container = ft.Stack([
            ft.Container(
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                            ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[ft.Column(
                                    margin=ft.margin.symmetric(horizontal=30),
                                    controls=[self.button_check, 
                                              self.button_compare,
                                              self.button_load]),
                                    
                            self.container_status
                            ]

                        ),]
                ),

                margin=ft.margin.only(top=10, left=20, right=20),
                border=ft.border.all(1, "white"),
                padding=ft.padding.symmetric(horizontal=40, vertical=10),
                border_radius=10,
            ),

            # Border and title
            ft.Container(
                content=ft.Text(value="| Load configuration |", bgcolor="#111418", color="white", size=12),
                margin=ft.margin.only(left=60),
            )

            ])
    
    def handle_check_communication(self, e):
        
        self.disable_buttons()
        self.text_status.value = "Checking communication... "
        self.container_status.bgcolor = ft.Colors.YELLOW
        self.text_status.update()
        self.container_status.update()
        self.disable_buttons()
        self.parent.page.run_thread(self.check_configuration_backup)

    def check_configuration_backup(self):
        if self.parent.frame_config.method == 0:
            com_to_stratix = get_switch_name(self.parent.stratix_selected)
            device = "C:/Users/Test/Desktop/Backups/" + com_to_stratix + "backup"
        else:
            device = "C:/Users/Test/Desktop/Backups/" + self.parent.stratix_selected + "backup"

        result = check_difference_config_backup(device, self.parent.stratix_network)

        self.parent.view_compare.backup_text = result[2]
        self.parent.view_compare.configuration_text = result[3]

        if result[0]:
            self.text_status.value = "File and configuration are the same!"
            self.container_status.bgcolor = ft.Colors.GREEN
            self.enable_buttons(1)
        else:
            match result[1]:
                case 0:
                    self.text_status.value = "Backup file and configuration are different! if you are sure that you want to load the configuration, please click the Load Configuration button."
                    self.container_status.bgcolor = ft.Colors.ORANGE_200
                    self.enable_buttons()
                case 1:
                    if self.parent.frame_config.method == 0:
                        self.text_status.value = "Stratix connection Error! Please check the serial connectionn"
                    else:
                        self.text_status.value = "Stratix connection Error! Please check the ethernet connection or SSH configuration"
                    self.container_status.bgcolor = ft.Colors.RED_400
                    self.enable_buttons(1)
                    self.enable_buttons(2)
                case 2:
                    self.text_status.value = "Empty backup file! Please check the backup file."
                    self.container_status.bgcolor = ft.Colors.RED_400
                    self.enable_buttons(1)
                case 3:
                    self.text_status.value = "Backup file does not exist! Please check the backup file."
                    self.container_status.bgcolor = ft.Colors.RED_400
                    self.enable_buttons(1)

        self.text_status.update()
        self.container_status.update()
        self.parent.view_compare.update_content_backup()

    def handle_load_configuration(self):
        self.text_status.value = "Downloading Configuration"
        self.container_status.bgcolor = ft.Colors.ORANGE_700
        self.disable_buttons()
        self.parent.frame_path.enable_disable_dd(True)
        self.parent.frame_serial.enable_disable_dd(True)
        self.parent.frame_config.enable_disable_dd(True)
        self.parent.page.run_thread(self.load_configuration_thread)

    def load_configuration_thread(self):

        if self.parent.frame_config.method == 0:
            com_to_stratix = get_switch_name(self.parent.stratix_selected)
            device = "C:/Users/Test/Desktop/Backups/" + com_to_stratix + "backup"
        else:
            device = "C:/Users/Test/Desktop/Backups/" + self.parent.stratix_selected + "backup"

        result = load_configuration(device, self.parent.stratix_network, self.parent.logger)

        if result:
            self.text_status.value = f"Configuration loaded successfully Waiting to restart the device! {self.parent.stratix_selected}"
            self.container_status.bgcolor = ft.Colors.AMBER_600
            self.parent.page.update()
            if self.parent.frame_config.method == 0:
                self.parent.page.run_thread(self.check_communication_update, com_to_stratix)
            else:
                self.parent.page.run_thread(self.check_communication_update, self.parent.stratix_selected)

        else:
            if self.parent.frame_config.method == 0:
                self.text_status.value = f"Error loading configuration! {self.parent.stratix_selected}, please check the serial connection"
            else:
                self.text_status.value = f"Error loading configuration! {self.parent.stratix_selected}, please check the connection with {self.parent.stratix_network['host']} or ssh configuration"
            self.container_status.bgcolor = ft.Colors.RED_600

            self.enable_buttons()
            self.parent.frame_path.enable_disable_dd(False)
            self.parent.frame_serial.enable_disable_dd(False)
            self.parent.frame_config.enable_disable_dd(False)

    def check_communication_update(self, stratix_name: str):

        contador = 0

        while contador < 180:
            sleep(1)
            contador +=1

        check_comm = checking_communication(stratix_name)

        if check_comm:
            self.text_status.value = f"Device available! {self.parent.stratix_selected}"
            self.container_status.bgcolor = ft.Colors.GREEN_600
        else:
            self.text_status.value = f"Error communicating with the device {self.parent.stratix_selected}, please check the Stratix"
            self.container_status.bgcolor = ft.Colors.RED_600

        self.enable_buttons()
        self.parent.frame_path.enable_disable_dd(False)
        self.parent.frame_serial.enable_disable_dd(False)
        self.parent.frame_config.enable_disable_dd(False)

    def disable_buttons(self, b_disable: int = None):
        if b_disable == 1 or b_disable == None:
            self.button_check.disabled = True
        if b_disable ==2 or b_disable == None:
            self.button_compare.disabled = True
        if b_disable ==3 or b_disable == None: 
            self.button_load.disabled = True
        self.parent.page.update()

    def enable_buttons(self, b_disable: int = None):
        if b_disable ==1 or b_disable == None:
            self.button_check.disabled = False
        if b_disable == 2 or b_disable == None:
            self.button_compare.disabled = False
        if b_disable ==3 or b_disable == None: 
            self.button_load.disabled = False
        self.parent.page.update()