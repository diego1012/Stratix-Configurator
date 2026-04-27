import flet as ft

class ViewCompare():

    def __init__(self, parent):

        self.parent = parent

        self.backup_text = []
        self.configuration_text = []

        self.column_backup = ft.Column(scroll=ft.ScrollMode.ALWAYS,
                                       margin=0,
                                       spacing=0,
                                       expand=True,
                                       controls=[])
        
        self.column_configuration = ft.Column(scroll=ft.ScrollMode.ALWAYS,
                                              margin=0,
                                              spacing=0,
                                              expand=True,
                                              controls=[])

        self.container = ft.Stack([
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[ft.Text("Comparison Backup VS Configuration", 
                                            color="white", size=16),
                                    ft.Button(content="Return", 
                                                bgcolor=ft.Colors.RED_400, 
                                                color=ft.Colors.WHITE, 
                                                icon=ft.Icons.EXIT_TO_APP, 
                                                icon_color=ft.Colors.WHITE, 
                                                style=ft.ButtonStyle(text_style=ft.TextStyle(size=12)),
                                                on_click=self.parent.show_previous_page)]),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            height=550,
                            controls=[
                                ft.Container(
                                    margin=ft.margin.only(top=5, left=5, right=5),
                                    border=ft.border.all(1, "white"),
                                    expand = True,
                                    border_radius=10,
                                    content=self.column_backup),
                                ft.Container(
                                    margin=ft.margin.only(top=2, left=5, right=5),
                                    border=ft.border.all(1, "white"),
                                    border_radius=10,
                                    expand = True,
                                    content=ft.Column(
                                        scroll=ft.ScrollMode.ALWAYS,
                                        controls=self.column_configuration
                                    ))
                                ]
                        )
                    ]
                ),

                margin=ft.margin.only(top=10, left=20, right=20),
                border=ft.border.all(1, "white"),
                padding=ft.padding.symmetric(horizontal=10, vertical=10),
                border_radius=10,
            ),

        ])

    def update_content_backup(self):

        self.column_backup.controls = []
        self.column_configuration.controls = []

        self.column_backup.update()
        self.column_configuration.update()

        num = 0

        for bk in self.backup_text:
            num +=1
            if num <= 9:
                space = " " * 6
            elif 10 <= num <= 99:
                space = " " * 5
            else:
                space = " " * 4
            self.column_backup.controls.append(
            ft.Container(bgcolor= ft.Colors.with_opacity(0.2, "red") if bk not in self.configuration_text else ft.Colors.TRANSPARENT, 
                        margin=0,
                        padding=0,
                        width=float("inf"),
                        content=ft.Text(f"{num}{space}{bk}", 
                                        size=10,
                                        margin=ft.margin.all(0))))

        num = 0

        for cf in self.configuration_text:
            num +=1
            if num <= 9:
                space = " " * 6
            elif 10 <= num <= 99:
                space = " " * 5
            else:
                space = " " * 4
            self.column_configuration.controls.append(
            ft.Container(bgcolor= ft.Colors.with_opacity(0.2, "red") if cf not in self.backup_text else ft.Colors.TRANSPARENT, 
                        margin=0,
                        padding=0,
                        width=float("inf"),
                        content=ft.Text(f"{num}{space}{cf}", 
                                        size=10,
                                        margin=ft.margin.all(0))))

        self.column_backup.update()
        self.column_configuration.update()
