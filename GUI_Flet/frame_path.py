import flet as ft
from functions import generate_dropdowns

class FramePath:

    def __init__(self, parent):

    # Dropdown for Stratix configuration path

        self.parent = parent

        self.stratix_information = generate_dropdowns(test=True)

        self.dd = ft.Dropdown(
                        editable=True,
                        label="Stratix",
                        options=self.get_options(),
                        text_size=12,
                        on_select = lambda e:self.handle_dropdown_change(e),
                        )


        self.container = ft.Stack([
            ft.Container(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                    ft.Text("Configuration Path", margin=ft.margin.only(right=20)),

                    ft.SafeArea(content=self.dd, margin=ft.margin.only(right=20)),

                    ft.Button(
                            content="Update Device List",
                            icon=ft.Icons.REFRESH,
                            color=ft.Colors.GREEN_400,
                            icon_color=ft.Colors.GREEN_400,
                            style=ft.ButtonStyle(text_style=ft.TextStyle(size=12)),
                            on_click=lambda e:self.reset_dropdown(),
                            )     
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
        self.parent.frame_load.enable_buttons(1)
        position = self.stratix_information[0].index(self.parent.stratix_selected)
        self.parent.stratix_network = self.stratix_information[1][position]
        self.parent.frame_load.disable_buttons(2)
        self.parent.frame_load.disable_buttons(3)

    def reset_dropdown(self):
        self.dd.value = None
        self.stratix_information = generate_dropdowns(test=True)
        self.dd.options = self.get_options()
        self.dd.update()
        self.parent.frame_config.enable_disable_dd(True)
        self.parent.frame_load.disable_buttons()

    def update_frame(self, e):
        self.parent.page.update()

    def disable_all(self):
        self.container.disabled = True
        self.parent.page.update()

    def enable_all(self):
        self.container.disabled = False
        self.parent.page.update()
