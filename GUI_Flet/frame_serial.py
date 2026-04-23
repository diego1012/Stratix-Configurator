import flet as ft

def get_options() -> list[ft.DropdownOption]:
    stratix = ["COM1", "COM2", "COM3"]
    return [
        ft.DropdownOption(
            key=st,
            content=ft.Text(value=st, color="white"),
        )
        for st in stratix
    ]

class FrameSerial():

    def __init__(self, parent):

        self.parent = parent

        self.dd = ft.Dropdown(
                        editable=True,
                        label="Port",
                        options=get_options(),
                        disabled= True
                        )

        self.container = ft.Stack([
            ft.Container(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                    ft.Text("Configuration Path", margin=ft.margin.only(right=20)),

                    ft.SafeArea(content=self.dd, margin=ft.margin.only(right=20)),

                    ft.Button(
                            content="Update port List",
                            icon=ft.Icons.REFRESH,
                            color=ft.Colors.GREEN_400,
                            icon_color=ft.Colors.GREEN_400,
                            style=ft.ButtonStyle(text_style=ft.TextStyle(size=12)),
                            on_click=self.reset_dropdown,
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
                content=ft.Text("| Serial Communication |", bgcolor="#111418", color="white", size=12),
                margin=ft.margin.only(left=60),
            )

            ])

    def reset_dropdown(self, e):
        self.dd.value = None
        self.dd.update()
        self.parent.frame_config.enable_disable_dd(True)

    def update_frame(self):
        self.dd.update()

    def enable_disable_dd(self,action: bool):
        self.dd.disabled = action
        self.update_frame()

    def disable_all(self):
        self.container.disabled = True
        self.parent.page.update()

    def enable_all(self):
        self.container.disabled = False
        self.parent.page.update()
    

