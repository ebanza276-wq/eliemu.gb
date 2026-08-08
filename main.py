import asyncio
import flet as ft
# --- Palette (rust / paper / sage / mustard) ---
RUST = "#E85D42"
RUST_DARK = "#C94A32"
PAPER = "#FAF6F1"
INK = "#2B2320"
MUTED = "#8A7F78"
GOLD = "#E8A93C"
CARD_BG = "#FFFFFF"
BORDER = "#EFE7E0"

CATEGORIES = [
    ("Tout", ft.Icons.APPS),
    ("Véhicules", ft.Icons.DIRECTIONS_CAR_FILLED_OUTLINED),
    ("Electronique", ft.Icons.DEVICES_OTHER_OUTLINED),
    ("Mode & Beauté", ft.Icons.CHECKROOM_OUTLINED),
    ("Immobilier", ft.Icons.HOME_WORK_OUTLINED),
    ("Electroménager", ft.Icons.KITCHEN_OUTLINED),
    ("Pour la maison", ft.Icons.CHAIR_OUTLINED),
    ("Emplois", ft.Icons.WORK_OUTLINE),
    ("Services", ft.Icons.MISCELLANEOUS_SERVICES_OUTLINED),
]

# Catégories utilisables dans le formulaire de dépôt (on exclut "Tout")
FORM_CATEGORIES = [c[0] for c in CATEGORIES if c[0] != "Tout"]

# Un seul schéma de données, cohérent entre la liste et le détail
ANNONCES = [
    {
        "title": "Nike air force one - first quality",
        "price": "Prix sur demande",
        "time": "13 heures",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/nike/400/300",
        "categorie": "Mode & Beauté",
        "date": "01 août 2026",
        "description": "Nike Air Force One first quality, taille unique, jamais portées.",
    },
    {
        "title": "Vente - parcelle à macampagne",
        "price": "475 000 USD",
        "time": "14 heures",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/parcelle/400/300",
        "categorie": "Immobilier",
        "date": "01 août 2026",
        "description": "Belle parcelle bien située, titre disponible, idéale pour construction.",
    },
    {
        "title": "Toyota rav4 2018",
        "price": "16 500 000 USD",
        "time": "16 heures",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/rav4/400/300",
        "categorie": "Véhicules",
        "date": "01 août 2026",
        "description": "Toyota RAV4 2018, très bon état, entretien à jour.",
    },
    {
        "title": "Toyota fortuner 2015",
        "price": "3 250 000 USD",
        "time": "16 heures",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/fortuner/400/300",
        "categorie": "Véhicules",
        "date": "01 août 2026",
        "description": "Toyota Fortuner 2015, moteur diesel, climatisation fonctionnelle.",
    },
    {
        "title": "ASUS Rog",
        "price": "200 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/asus/400/300",
        "categorie": "Electronique",
        "date": "31 juillet 2026",
        "description": "PC portable gamer ASUS ROG, bon état, chargeur inclus.",
    },
    {
        "title": "Chinelas de homem",
        "price": "Prix sur demande",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/chinelas/400/300",
        "categorie": "Mode & Beauté",
        "date": "31 juillet 2026",
        "description": "Sandales homme, plusieurs pointures disponibles.",
    },
    {
        "title": "Yamaha mt 09 2026",
        "price": "2 000 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/mt09/400/300",
        "categorie": "Véhicules",
        "date": "31 juillet 2026",
        "description": "Yamaha MT-09 2026, très peu de kilomètres, comme neuve.",
    },
    {
        "title": "Yamaha mt 03 2026",
        "price": "1 500 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/mt03/400/300",
        "categorie": "Véhicules",
        "date": "31 juillet 2026",
        "description": "Yamaha MT-03 2026, idéale pour débutants, papiers en règle.",
    },
    {
        "title": "Oppo reno 16",
        "price": "170 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/oppo/400/300",
        "categorie": "Electronique",
        "date": "31 juillet 2026",
        "description": "Oppo Reno 16, 256 Go, sous garantie, accessoires d'origine.",
    },
]


def main(page: ft.Page):
    page.title = "Annonces"
    page.bgcolor = PAPER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.width = 390
    page.window.height = 844
    page.window.icon = "assets/icon.png"
    page.scroll = ft.ScrollMode.AUTO
    page.fonts = {
        "Fraunces": "https://raw.githubusercontent.com/googlefonts/fraunces/main/fonts/variable/Fraunces%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf"
    }
    # state["selected"] garde l'annonce actuellement ouverte en détail
    state = {"query": "", "categorie": "Tout", "selected": None}
    favorites = set()

    # ---------- Header ----------
    search_field = ft.TextField(
        hint_text="Chercher sur Annonces...",
        border_radius=30,
        bgcolor="#F3EEE9",
        border_color="transparent",
        focused_border_color=RUST,
        content_padding=ft.Padding.symmetric(horizontal=18, vertical=8),
        height=42,
        expand=True,
        suffix_icon=ft.Icons.SEARCH,
        on_submit=lambda e: show_list(search_field.value),
    )

    def go_to_publier(e=None):
        asyncio.create_task(page.push_route("/publier"))

    header = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
        bgcolor=CARD_BG,
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.LOCATION_ON, color="white", size=22),
                    bgcolor=RUST,
                    border_radius=10,
                    padding=8,
                ),
                ft.Container(search_field, expand=True),
                ft.IconButton(ft.Icons.CURRENCY_EXCHANGE, icon_color=INK),
                ft.CircleAvatar(
                    content=ft.Icon(ft.Icons.PERSON, color="white"),
                    bgcolor=MUTED,
                    radius=18,
                ),
            ],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # ---------- Hero banner ----------
    hero = ft.Container(
        height=170,
        border_radius=0,
        gradient=ft.LinearGradient(
            colors=[RUST, RUST_DARK],
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
        ),
        padding=ft.Padding.symmetric(horizontal=28, vertical=20),
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Achète facile", size=30, weight=ft.FontWeight.W_600,
                                font_family="Fraunces", color="white", italic=True),
                        ft.Text("Vends rapide", size=30, weight=ft.FontWeight.W_600,
                                font_family="Fraunces", color="white", italic=True),
                    ],
                    spacing=0,
                ),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.PHONE_IPHONE, size=90, color="#FFFFFF33"),
            ],
        ),
    )

    def filter_by_category(name):
        state["categorie"] = name
        show_list(search_field.value, category=name if name != "Tout" else None)

    def category_item(name, icon):
        selected = name == state["categorie"]
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=16, color="#FFFFFF" if selected else RUST_DARK),
                    ft.Text(name, size=13, color="#FFFFFF" if selected else "#3A3A3A", weight=ft.FontWeight.W_500),
                ],
                spacing=6,
                tight=True,
            ),
            bgcolor=RUST if selected else "#FFFFFF",
            border=ft.Border.all(1, RUST if selected else BORDER),
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            on_click=lambda e, n=name: filter_by_category(n),
            ink=True,
        )

    def build_category_row():
        return ft.Row(
            [category_item(n, i) for n, i in CATEGORIES]
            + [
                ft.Container(
                    content=ft.Icon(ft.Icons.CHEVRON_RIGHT, color="white"),
                    bgcolor=RUST,
                    border_radius=20,
                    padding=10,
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=6,
        )

    category_row = ft.Container(
        padding=ft.Padding.symmetric(horizontal=12, vertical=14),
        bgcolor=CARD_BG,
        content=build_category_row(),
    )

    # ---------- Bouton "Déposer une annonce" ----------
    deposer_banner = ft.Container(
        margin=ft.Padding.symmetric(horizontal=16, vertical=6),
        content=ft.ElevatedButton(
            "Déposer une annonce",
            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
            style=ft.ButtonStyle(
                bgcolor=RUST,
                color="#FFFFFF",
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding.symmetric(horizontal=20, vertical=16),
            ),
            width=float("inf"),
            on_click=go_to_publier,
        ),
    )

    # ---------- Ad banner ----------
    ad_banner = ft.Container(
        margin=ft.Padding.symmetric(horizontal=16, vertical=14),
        padding=14,
        border_radius=12,
        bgcolor=CARD_BG,
        border=ft.Border.all(1, BORDER),
        content=ft.Column(
            [
                ft.Text("Publicité", size=11, color=MUTED),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Activate Registration", size=18,
                                        weight=ft.FontWeight.BOLD, color=INK),
                            ],
                            expand=True,
                        ),
                        ft.ElevatedButton(
                            "OPEN",
                            bgcolor=GOLD,
                            color="white",
                            icon=ft.Icons.ARROW_FORWARD_IOS,
                        ),
                    ]
                ),
            ]
        ),
    )

    def go_to_detail(item):
        # Mémorise l'annonce cliquée AVANT de changer de route, sinon
        # la vue "/details" ne sait pas quelle annonce afficher.
        state["selected"] = item
        asyncio.create_task(page.push_route("/details"))

    def listing_card(item):
        is_fav = ft.Ref[ft.IconButton]()

        def toggle_fav(e):
            key = item["title"]
            if key in favorites:
                favorites.discard(key)
                is_fav.current.icon = ft.Icons.FAVORITE_BORDER
                is_fav.current.icon_color = INK
            else:
                favorites.add(key)
                is_fav.current.icon = ft.Icons.FAVORITE
                is_fav.current.icon_color = RUST
            is_fav.current.update()

        price_color = RUST if "USD" in item["price"] else GOLD

        return ft.Container(
            width=210,
            bgcolor=CARD_BG,
            border=ft.Border.all(1, BORDER),
            border_radius=14,
            on_click=lambda e, it=item: go_to_detail(it),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Column(
                [
                    ft.Stack(
                        [
                            ft.Image(src=item["img"], height=140, width=210, fit="cover"),
                            ft.Container(
                                content=ft.Row(
                                    [ft.Icon(ft.Icons.ACCESS_TIME, size=12, color="white"),
                                     ft.Text(item["time"], size=11, color="white")],
                                    spacing=4,
                                ),
                                bgcolor="#00000099",
                                border_radius=20,
                                padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                                top=8, left=8,
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    ref=is_fav,
                                    icon=ft.Icons.FAVORITE_BORDER,
                                    icon_color=INK,
                                    icon_size=18,
                                    bgcolor="white",
                                    on_click=toggle_fav,
                                ),
                                top=6, right=6,
                            ),
                        ]
                    ),
                    ft.Container(
                        padding=ft.Padding.symmetric(horizontal=10, vertical=8),
                        content=ft.Column(
                            [
                                ft.Text(item["price"], size=14, weight=ft.FontWeight.BOLD,
                                        color=price_color),
                                ft.Text(item["title"], size=12.5, color=INK, max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Row(
                                    [ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=13, color=MUTED),
                                     ft.Text(item["loc"], size=11, color=MUTED)],
                                    spacing=2,
                                ),
                            ],
                            spacing=3,
                        ),
                    ),
                ],
                spacing=0,
            ),
        )

    grid = ft.GridView(
        expand=True,
        runs_count=0,
        max_extent=230,
        child_aspect_ratio=0.72,
        spacing=12,
        run_spacing=12,
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        controls=[listing_card(a) for a in ANNONCES],
    )

    def show_list(query=None, category=None):
        # On garde l'état de catégorie synchronisé, que l'appel vienne
        # d'un clic sur une puce ou d'une recherche.
        if category is not None:
            state["categorie"] = category
        state["query"] = query or ""

        items = ANNONCES
        if state["categorie"] and state["categorie"] != "Tout":
            items = [a for a in items if a["categorie"] == state["categorie"]]
        if state["query"]:
            q = state["query"].lower()
            items = [a for a in items if q in a["title"].lower()]

        grid.controls = [listing_card(a) for a in items]
        # On régénère la barre de catégories pour que la puce sélectionnée
        # reflète bien state["categorie"].
        category_row.content = build_category_row()
        content_area.controls = [header, hero, category_row, deposer_banner, ad_banner, grid, ft.Container(height=20)]
        content_area.update()

    content_area = ft.Column(
        [header, hero, category_row, deposer_banner, ad_banner, grid, ft.Container(height=20)],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def build_detail_view(annonce):
        """Construit et RENVOIE le contenu de la page détail (ne modifie
        plus content_area directement, pour pouvoir servir de contrôle
        dans la ft.View('/details'))."""
        return ft.Column(
            [
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Container(
                                content=ft.Image(
                                    src=annonce["img"],
                                    fit="cover",
                                    border_radius=12,
                                    height=340,
                                ),
                                col={"sm": 12, "md": 7},
                            ),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            annonce["price"],
                                            size=28,
                                            weight=ft.FontWeight.BOLD,
                                            color=RUST_DARK,
                                        ),
                                        ft.Text(annonce["title"], size=20, weight=ft.FontWeight.W_600),
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=16, color=MUTED),
                                                ft.Text(annonce["loc"], color=MUTED),
                                            ],
                                            spacing=4,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Container(
                                                    content=ft.Text(annonce["categorie"], size=12, color=RUST_DARK),
                                                    bgcolor="#F6E4DC",
                                                    padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                                                    border_radius=20,
                                                ),
                                                ft.Text(annonce["date"], size=12, color=MUTED),
                                            ],
                                            spacing=10,
                                        ),
                                        ft.Divider(color=BORDER),
                                        ft.Text("Description", weight=ft.FontWeight.W_600),
                                        ft.Text(annonce["description"], color="#5A5A5A"),
                                        ft.Divider(color=BORDER),
                                        ft.ElevatedButton(
                                            "Contacter le vendeur",
                                            icon=ft.Icons.CHAT_BUBBLE_OUTLINE,
                                            style=ft.ButtonStyle(
                                                bgcolor=RUST,
                                                color="#FFFFFF",
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                                padding=ft.Padding.symmetric(horizontal=20, vertical=14),
                                            ),
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                col={"sm": 12, "md": 5},
                                padding=ft.Padding.only(left=16),
                            ),
                        ],
                    ),
                    padding=24,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    # ---------- Formulaire "Déposer une annonce" ----------
    def build_publier_view():
        title_field = ft.TextField(label="Titre de l'annonce", border_radius=10, bgcolor=CARD_BG)
        price_field = ft.TextField(
            label="Prix (ex: 200 USD ou Prix sur demande)", border_radius=10, bgcolor=CARD_BG
        )
        loc_field = ft.TextField(
            label="Localisation", value="Kinshasa, RDC", border_radius=10, bgcolor=CARD_BG
        )
        desc_field = ft.TextField(
            label="Description",
            multiline=True,
            min_lines=4,
            max_lines=8,
            border_radius=10,
            bgcolor=CARD_BG,
        )
        category_dropdown = ft.Dropdown(
            label="Catégorie",
            options=[ft.dropdown.Option(c) for c in FORM_CATEGORIES],
            value=FORM_CATEGORIES[0],
            border_radius=10,
            bgcolor=CARD_BG,
        )
        error_text = ft.Text("", color=RUST, size=12)

        # ---------- Aperçu photo piloté par l'URL ----------
        placeholder_photo = ft.Column(
            [
                ft.Icon(ft.Icons.ADD_PHOTO_ALTERNATE_OUTLINED, size=40, color=MUTED),
                ft.Text("Colle une URL d'image ci-dessous pour l'aperçu", size=12, color=MUTED),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        )
        photo_box = ft.Container(
            height=180,
            border_radius=14,
            bgcolor="#F3EEE9",
            border=ft.Border.all(1, BORDER),
            alignment=ft.Alignment.CENTER,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=placeholder_photo,
        )

        def update_preview(e):
            url = (img_field.value or "").strip()
            if url:
                photo_box.content = ft.Image(src=url, height=180, width=1000, fit="cover")
            else:
                photo_box.content = placeholder_photo
            photo_box.update()

        img_field = ft.TextField(
            label="URL de l'image (optionnel)",
            border_radius=10,
            bgcolor=CARD_BG,
            on_change=update_preview,
        )

        def section_card(titre, controls_list):
            return ft.Container(
                padding=18,
                border_radius=16,
                bgcolor=CARD_BG,
                border=ft.Border.all(1, BORDER),
                content=ft.Column(
                    [ft.Text(titre, size=15, weight=ft.FontWeight.BOLD, color=INK), *controls_list],
                    spacing=12,
                ),
            )

        def annuler(e):
            asyncio.create_task(page.push_route("/"))

        def publier(e):
            manquants = []
            if not (title_field.value or "").strip():
                manquants.append("le titre")
            if not (price_field.value or "").strip():
                manquants.append("le prix")
            if not (desc_field.value or "").strip():
                manquants.append("la description")

            if manquants:
                error_text.value = "Merci de renseigner : " + ", ".join(manquants)
                error_text.update()
                return

            error_text.value = ""
            nouvelle_annonce = {
                "title": title_field.value.strip(),
                "price": price_field.value.strip(),
                "time": "à l'instant",
                "loc": (loc_field.value or "Kinshasa, RDC").strip(),
                "img": (img_field.value or "").strip()
                or f"https://picsum.photos/seed/{len(ANNONCES)}/400/300",
                "categorie": category_dropdown.value,
                "date": "Aujourd'hui",
                "description": desc_field.value.strip(),
            }
            ANNONCES.insert(0, nouvelle_annonce)
            show_list()
            asyncio.create_task(page.push_route("/"))

        # Largeur max du formulaire : plein écran sur mobile, colonne
        # centrée et resserrée sur des écrans plus larges (desktop/web).
        form_width = min(page.width or 480, 480)

        form_header = ft.Container(
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
            bgcolor=CARD_BG,
            alignment=ft.Alignment.CENTER,
            content=ft.Container(
                width=form_width,
                content=ft.Row(
                    [
                        ft.IconButton(ft.Icons.ARROW_BACK, icon_color=INK, on_click=annuler),
                        ft.Container(
                            content=ft.Text(
                                "Déposer une annonce",
                                size=18,
                                weight=ft.FontWeight.W_600,
                                font_family="Fraunces",
                                color=INK,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            expand=True,
                            alignment=ft.Alignment.CENTER,
                        ),
                        # espace fantôme pour équilibrer le bouton retour
                        # et garder le titre visuellement centré
                        ft.Container(width=48),
                    ],
                    spacing=6,
                ),
            ),
        )

        body = ft.Column(
            [
                ft.Container(
                    photo_box, margin=ft.Margin.symmetric(horizontal=16, vertical=8)
                ),
                ft.Container(
                    section_card(
                        "Informations générales",
                        [title_field, price_field, category_dropdown, loc_field, img_field],
                    ),
                    margin=ft.Margin.symmetric(horizontal=16, vertical=8),
                ),
                ft.Container(
                    section_card("Description", [desc_field]),
                    margin=ft.Margin.symmetric(horizontal=16, vertical=8),
                ),
                ft.Container(error_text, margin=ft.Margin.symmetric(horizontal=16)),
                ft.Container(
                    ft.ElevatedButton(
                        "Publier l'annonce",
                        icon=ft.Icons.PUBLISH,
                        style=ft.ButtonStyle(
                            bgcolor=RUST,
                            color="#FFFFFF",
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.Padding.symmetric(horizontal=20, vertical=16),
                        ),
                        width=float("inf"),
                        on_click=publier,
                    ),
                    margin=ft.Margin.symmetric(horizontal=16, vertical=6),
                ),
                ft.Container(
                    ft.OutlinedButton(
                        "Annuler",
                        style=ft.ButtonStyle(
                            color=INK, shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                        width=float("inf"),
                        on_click=annuler,
                    ),
                    margin=ft.Padding.symmetric(horizontal=16),
                ),
                ft.Container(height=24),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        centered_body = ft.Container(
            content=body,
            width=form_width,
            expand=True,
        )

        return ft.Container(
            expand=True,
            bgcolor=PAPER,
            content=ft.Column(
                [
                    form_header,
                    ft.Container(
                        content=centered_body,
                        alignment=ft.Alignment.TOP_CENTER,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
        )

    def route_change(e=None):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[content_area],
                bgcolor=PAPER,
            )
        )
        if page.route == "/details":
            # state["selected"] est renseigné par go_to_detail() au clic
            # sur une carte ; si jamais on arrive ici sans sélection
            # (ex. accès direct à l'URL), on retombe sur la première annonce.
            annonce = state["selected"] or ANNONCES[0]
            page.views.append(
                ft.View(
                    route="/details",
                    controls=[build_detail_view(annonce)],
                    bgcolor=PAPER,
                )
            )
        elif page.route == "/publier":
            page.views.append(
                ft.View(
                    route="/publier",
                    controls=[build_publier_view()],
                    bgcolor=PAPER,
                )
            )
        page.update()

    async def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Appel direct, PAS via page.go(), pour forcer l'affichage initial
    route_change()

ft.run(main)#, view=ft.AppView.WEB_BROWSER)
