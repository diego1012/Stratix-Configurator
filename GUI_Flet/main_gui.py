import flet as ft
from GUI_Flet import FramePath
from GUI_Flet import FrameConfig
from GUI_Flet import FrameSerial
from GUI_Flet import FrameLoad
from GUI_Flet import ViewCompare
from functions import create_logger 

class GUI ():

    def __init__(self, page:ft.page):

        self.page = page
        self.logger = create_logger(True)

        self.page.title = "Stratix Configuration"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.width = 630
        self.page.window.height = 700
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.frame_config = FrameConfig(self)
        self.frame_path = FramePath(self)
        self.frame_serial = FrameSerial(self)
        self.frame_load = FrameLoad(self)
        self.view_compare = ViewCompare(self)

        # Variables for application

        self.stratix_selected = None
        self.stratix_network = None


        self.general_view = ft.PageView(
                            expand=True,
                            viewport_fraction=1,
                            selected_index=0,
                            horizontal=True,
                            controls=[ft.Container(content = ft.Column(
                                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Text("Stratix Configurator",color="white", size=24),
                                                                    self.frame_config.container,
                                                                    self.frame_path.container, 
                                                                    self.frame_serial.container, 
                                                                    self.frame_load.container])),
                                    
                                     self.view_compare.container       
                                    ]

                        )

        page.add(
                ft.SafeArea(
                    expand=True,
                    content=(
                        self.general_view
                    ),
                ),
            )
        
        # initial disable status

        self.frame_path.container.disabled = True
        self.page.update()

    async def show_previous_page(self, e: ft.Event[ft.FloatingActionButton]):
        self.page.window.width = 630
        await self.general_view.previous_page(
            animation_curve=ft.AnimationCurve.EASE_OUT,
            animation_duration=ft.Duration(milliseconds=300),
        )
        self.page.update()

    async def show_next_page(self, e: ft.Event[ft.FloatingActionButton]):
        self.page.window.width = 1600
        await self.general_view.next_page(
            animation_curve=ft.AnimationCurve.EASE_OUT,
            animation_duration=ft.Duration(milliseconds=300),
        )
        self.page.update()
