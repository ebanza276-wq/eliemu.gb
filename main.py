import flet as ft
import base64

def main(page: ft.Page):

    image = ft.Image(
        src="",
        width=300,
        height=300,
    )

    async def handle_get_directory_path(e: ft.Event[ft.Button]):
        files = await ft.FilePicker().pick_files(
        allow_multiple=False,
        allowed_extensions=["png", "jpg", "jpeg"]
        )
    
        if files:
            with open(files[0].path, "rb") as f:
                image.src = base64.b64encode(f.read()).decode()
            page.update()

    page.add(
        ft.Button(
            content="Choisir une photo",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=handle_get_directory_path,
        ),
        image
    )

ft.app(main)
