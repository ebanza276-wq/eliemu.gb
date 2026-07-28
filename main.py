import flet as ft


def main(page: ft.Page):
    page.title = "Annonces"
    page.bgcolor = "#F5F5F7"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.window.width = 1366
    page.window.height = 768

    # ---------------- HEADER ----------------

    header = ft.Container(
        height=90,
        bgcolor="#1C1145",
        padding=30,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Annonces",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#7C4DFF",
                ),
                ft.Container(
                    width=420,
                    height=45,
                    bgcolor="white",
                    border_radius=12,
                    padding=15,
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SEARCH, color="grey"),
                            ft.Text(
                                "Rechercher une annonce...",
                                color="grey",
                            ),
                        ]
                    ),
                ),
                ft.Row(
                    spacing=20,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.TUNE, color="white"),
                                ft.Text("Filtres avancés", color="white"),
                            ]
                        ),
                        ft.ElevatedButton("Publier une annonce"),
                        ft.Icon(ft.Icons.NOTIFICATIONS_NONE, color="white"),
                        ft.Column(
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(
                                    ft.Icons.PERSON_OUTLINE,
                                    color="white",
                                ),
                                ft.Text(
                                    "Mon Profil",
                                    size=12,
                                    color="white",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )

    # ---------------- BANNIERE ----------------

    banner = ft.Container(
        height=120,
        border_radius=20,
        padding=25,
        gradient=ft.LinearGradient(
            colors=["#7C4DFF", "#D1B3FF"],
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    spacing=5,
                    controls=[
                        ft.Text(
                            "Trouvez ce dont vous avez besoin",
                            size=22,
                            color="white",
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Des milliers d'annonces près de chez vous",
                            color="white",
                        ),
                    ],
                ),
                ft.Text("🛋️", size=60),
            ],
        ),
    )

    # ---------------- CATEGORIES ----------------

    def categorie(icon, nom):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=70,
                    height=70,
                    border_radius=35,
                    bgcolor="#EEEEF4",
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text(icon, size=30),
                ),
                ft.Text(nom),
            ],
        )

    categories = ft.Row(
        spacing=35,
        controls=[
            categorie("🏠", "Immobilier"),
            categorie("🚗", "Véhicules"),
            categorie("💻", "Électronique"),
            categorie("🛋️", "Maison"),
            categorie("👕", "Mode"),
        ],
    )

    # ---------------- CARTE ----------------

    def card(image_url, prix, titre, ville):
        return ft.Container(
            width=200,
            bgcolor="white",
            border_radius=15,
            shadow=ft.BoxShadow(
                blur_radius=8,
                color="#DDDDDD",
            ),
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Stack(
                        controls=[
                            ft.Image(
                                src=image_url,
                                width=200,
                                height=140,
                                fit="cover",
                            ),
                            ft.Container(
                                top=8,
                                right=8,
                                width=32,
                                height=32,
                                bgcolor="white",
                                border_radius=16,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Icon(
                                    ft.Icons.FAVORITE_BORDER,
                                    size=18,
                                    color="#B05A6E",
                                ),
                            ),
                        ]
                    ),
                    ft.Container(
                        padding=12,
                        content=ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(
                                    prix,
                                    size=17,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    titre,
                                    size=15,
                                ),
                                ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.Icon(
                                            ft.Icons.LOCATION_ON_OUTLINED,
                                            size=15,
                                            color="grey",
                                        ),
                                        ft.Text(
                                            ville,
                                            size=13,
                                            color="grey",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    # ---------------- ANNONCES ----------------

    annonces = ft.GridView(
        runs_count=4,
        child_aspect_ratio=1.15,
        spacing=15,
        run_spacing=15,
        expand=True,
        controls=[
            card(
                "https://picsum.photos/500/300?1",
                "250 €",
                "Canapé 3 places",
                "Paris",
            ),
            card(
                "https://picsum.photos/500/300?2",
                "8 500 €",
                "Peugeot 208 2019",
                "Lyon",
            ),
            card(
                "https://picsum.photos/500/300?3",
                "320 €",
                "iPhone 11 64 Go",
                "Bordeaux",
            ),
            card(
                "https://picsum.photos/500/300?4",
                "900 €",
                "iPhone 15",
                "Bordeaux",
            ),
            card(
                "https://picsum.photos/500/300?5",
                "120 €",
                "Table en bois",
                "Nantes",
            ),
            card(
                "https://picsum.photos/500/300?6",
                "60 €",
                "Chaise design",
                "Marseille",
            ),
        ],
    )

    # ---------------- PAGE ----------------

    page.add(
        header,
        ft.Container(
            padding=30,
            content=ft.Column(
                controls=[
                    banner,
                    ft.Container(height=25),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Catégories",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Voir tout",
                                color="#7C4DFF",
                            ),
                        ],
                    ),
                    ft.Container(height=15),
                    categories,
                    ft.Container(height=30),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Annonces récentes",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Voir tout",
                                color="#7C4DFF",
                            ),
                        ],
                    ),
                    ft.Container(height=15),
                    annonces,
                ],
            ),
        ),
    )


ft.app(target=main)
