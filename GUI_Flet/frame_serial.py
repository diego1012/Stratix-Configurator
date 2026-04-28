import flet as ft
from functions import generate_dropdowns
from time import sleep

class FrameSerial():

    def __init__(self, parent):

        self.parent = parent
        self.port_data = None

        self.stratix_information = generate_dropdowns(logger = self.parent.logger, serial = True, test = True)

        self.dd = ft.Dropdown(
                        editable=False,
                        label="Port",
                        options=self.get_options(),
                        on_select=self.port_selected,
                        )

        self.update_button = ft.Button(
                            content="Update port List",
                            icon=ft.Icons.REFRESH,
                            style=ft.ButtonStyle(
                                    text_style={ft.ControlState.DEFAULT: ft.TextStyle(size=12, weight=ft.FontWeight.BOLD),
                                                ft.ControlState.DISABLED: ft.TextStyle(size=12)},
                                    padding=ft.padding.symmetric(vertical=3, horizontal=20),
                                    color={ft.ControlState.DEFAULT: ft.Colors.GREEN_400,
                                            ft.ControlState.DISABLED: ft.Colors.WHITE_70},
                                    bgcolor={ft.ControlState.DISABLED: ft.Colors.GREY_900},
                                    side= {ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.WHITE_60),
                                        ft.ControlState.DISABLED: ft.BorderSide(1, ft.Colors.TRANSPARENT)},
                                    icon_color={ft.ControlState.DEFAULT: ft.Colors.GREEN_400,
                                                ft.ControlState.DISABLED: ft.Colors.WHITE_70}
                                    ),
                            on_click= lambda e: self.reset_dropdown(),
                            )  

        self.wait_dialog =ft.AlertDialog(
            modal = True,
            content=ft.Column(
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[ft.ProgressRing(
                    color = ft.Colors.ORANGE_700,
                    padding=ft.padding.symmetric(vertical=10)),
                        
                        ft.Text("Loading serial ports")]))

        self.container = ft.Stack([
            ft.Container(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                    ft.Text("Configuration Path", margin=ft.margin.only(right=20)),

                    ft.SafeArea(content=self.dd, margin=ft.margin.only(right=20)),

                    self.update_button

                    ]
                ),
            margin=ft.margin.only(top=10, left=20, right=20),
            border=ft.border.all(1, "white"),
            padding=ft.padding.symmetric(horizontal=40, vertical=10),
            border_radius=10,
            ),

            # Border and title
            ft.Container(
                content=ft.Text("| Serial Communication |", bgcolor="#111418", color="white", size=12),
                margin=ft.margin.only(left=60),
            )

            ])

    def get_options(self,) -> list[ft.DropdownOption]:
        ports = self.stratix_information[0]
        return [
            ft.DropdownOption(
                key=pt,
                content=ft.Text(value=pt, color="white"),
            )
            for pt in ports
    ]

    def reset_dropdown(self):
        self.parent.page.show_dialog(self.wait_dialog)
        self.parent.page.run_thread(self.loading_message)

    def loading_message(self):
        self.dd.value = None
        self.port_data = None
        self.stratix_information = generate_dropdowns(logger = self.parent.logger, serial = True, test = True)
        self.dd.options = self.get_options()
        self.dd.update()
        sleep(3)
        self.parent.page.pop_dialog()
        self.parent.frame_load.disable_buttons()

    def port_selected(self):
        
        """
        This function gets the value from port dropdown and enable buttons if other selections are correct.

        """

        self.port_data = self.dd.value
        self.parent.frame_load.enable_buttons(1)
        self.parent.frame_load.disable_buttons(2)
        self.parent.frame_load.disable_buttons(3)

        self.parent.stratix_selected = self.port_data
        self.parent.frame_config.enable_disable_dd(False)
        position = self.stratix_information[0].index(self.parent.stratix_selected)
        self.parent.stratix_network = self.stratix_information[1][position]

    def update_frame(self):
        self.parent.page.update()

    def enable_disable_dd(self, action: bool):
        self.container.disabled = action
        self.update_frame()


