import flet as ft

def get_options() -> list[ft.DropdownOption]:
    stratix = ["Serial", "SSH", "Both"]
    return [
        ft.DropdownOption(
            key=st,
            content=ft.Text(value=st, color="white"),
        )
        for st in stratix
    ]

class FrameConfig():

    def __init__(self, parent):

        self.parent = parent
        self.status_dd = True

        self.dd = ft.Dropdown(
                        editable=True,
                        label="Method",
                        options=get_options(),
                        disabled= True,
                        on_select=self.handle_dropdown_select
                        )

        self.container = ft.Stack([
            ft.Container(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ft.SafeArea(content=self.dd) ]

                ),

                margin=ft.margin.only(top=10, left=20, right=20),
                border=ft.border.all(1, "white"),
                padding=ft.padding.symmetric(horizontal=40, vertical=10),
                border_radius=10,
            ),

            # Border and title
            ft.Container(
                content=ft.Text("| Communication Method |", bgcolor="#111418", color="white", size=12),
                margin=ft.margin.only(left=60),
            )

            ])
        
    def handle_dropdown_select(self, e: ft.Event[ft.Dropdown]):
        if e.control.value == 'Serial':
            self.parent.frame_serial.enable_disable_dd(False)
        else:
            self.parent.frame_serial.enable_disable_dd(True)

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