import flet as ft
from functions import generate_dropdowns

class FramePath:

    def __init__(self, parent):

    # Dropdown for Stratix configuration path

        self.parent = parent

        self.stratix_information = generate_dropdowns(logger= self.parent.logger, test = True)

        self.dd = ft.Dropdown(
                        editable=False,
                        label="Stratix",
                        options=self.get_options(),
                        text_size=12,
                        on_select = lambda e:self.handle_dropdown_change(e),
                        )

        self.update_button = ft.Button(
                            content="Update Device List",
                            icon=ft.Icons.REFRESH,
                            style=ft.ButtonStyle(text_style={ft.ControlState.DEFAULT: ft.TextStyle(size=12, weight=ft.FontWeight.BOLD),
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

                            on_click=lambda e:self.reset_dropdown(),
                            ) 

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
                content=ft.Text("| Configuration Path |", bgcolor="#111418", color="white", size=12),
                margin=ft.margin.only(left=60),
            )

        ])

    def get_options(self) -> list[ft.DropdownOption]:
        return [
            ft.DropdownOption(
                key=st,
                content=ft.Text(value=st, color="white", size=12),
            )
            for st in self.stratix_information[0]
        ]

    def handle_dropdown_change(self, e):
        self.parent.stratix_selected = e.control.value
        self.parent.frame_config.enable_disable_dd(False)
        position = self.stratix_information[0].index(self.parent.stratix_selected)
        self.parent.stratix_network = self.stratix_information[1][position]
        
        # disabled buttons if configurations are correct
        if self.parent.frame_config.method == 1 or (self.parent.frame_config.method == 0 and self.parent.frame_serial.port_data is not None):
            self.parent.frame_load.enable_buttons(1)
            self.parent.frame_load.disable_buttons(2)
            self.parent.frame_load.disable_buttons(3)

        if self.parent.frame_config.method == 0:
            self.parent.frame_serial.enable_disable_dd(False)
                
    def reset_dropdown(self):
        self.dd.value = None
        self.stratix_information = generate_dropdowns(logger= self.parent.logger, test=True)
        self.dd.options = self.get_options()
        self.dd.update()
        #self.parent.frame_serial.enable_disable_dd(True)
        self.parent.frame_load.disable_buttons()

    def enable_disable_dd(self, action: bool):
        self.container.disabled = action
        self.update_frame()

    def update_frame(self):
        self.parent.page.update()
