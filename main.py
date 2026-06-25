import flet as ft

def main(page: ft.Page):
    page.title = "Mon application Flet"

    compteur = ft.Text(value="0", size=30)

    def incrementer(e):
        compteur.value = str(int(compteur.value) + 1)
        page.update()

    bouton = ft.ElevatedButton(
        "Cliquez ici",
        on_click=incrementer
    )

    page.add(
        ft.Text("Exemple Flet"),
        compteur,
        bouton
    )

ft.app(target=main, view="web_browser")
