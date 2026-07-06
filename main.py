import flet as ft
import flet_camera as fc

def main(page: ft.Page):
    camera = fc.Camera()

    page.add(
        camera
    )

ft.app(main)
