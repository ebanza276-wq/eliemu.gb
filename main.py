import flet as ft
import asyncio

# ---------------------------------------------------------------------------
# PALETTE (nettoyée — une seule source de vérité, plus de doublons)
# ---------------------------------------------------------------------------
PRIMARY = "#2954E5"       # bleu de marque (logo, CTA principal)
PRIMARY_DARK = "#1E3FBF"
RUST = "#E85D42"          # accent prix / favoris
RUST_DARK = "#C94A32"
GOLD = "#E8A93C"           # accent pub / prix "sur demande"
PAPER = "#FAF6F1"          # fond général, chaud
CARD_BG = "#FFFFFF"
INK = "#2B2320"             # texte principal (chaud, pas noir pur)
MUTED = "#8A7F78"           # texte secondaire
BORDER = "#EFE7E0"
CHIP_BG = "#F3EEE9"

CATEGORIES = [
    ("Tout", ft.Icons.APPS),
    ("Immobilier", ft.Icons.HOME_OUTLINED),
    ("Véhicules", ft.Icons.DIRECTIONS_CAR_OUTLINED),
    ("Électronique", ft.Icons.PHONE_IPHONE_OUTLINED),
    ("Maison & Jardin", ft.Icons.YARD_OUTLINED),
    ("Mode & Beauté", ft.Icons.CHECKROOM_OUTLINED),
]

ANNONCES = [
    {
        "title": "Nike Air Force One - first quality",
        "price": "Prix sur demande",
        "time": "13 heures",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/nike/400/300",
        "categorie": "Mode & Beauté",
        "date": "01 août 2026",
        "description": "Nike Air Force One first quality, taille unique, jamais portées.",
    },
    {
        "title": "Toyota RAV4 2018",
        "price": "16 500 USD",
        "time": "16 heures",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/rav4/400/300",
        "categorie": "Véhicules",
        "date": "01 août 2026",
        "description": "Toyota RAV4 2018, bon état général, entretien à jour, climatisation fonctionnelle.",
    },
    {
        "title": "ASUS ROG",
        "price": "200 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/asus/400/300",
        "categorie": "Électronique",
        "date": "01 août 2026",
        "description": "PC portable gamer ASUS ROG, bon état, chargeur inclus.",
    },
    {
        "title": "Oppo Reno 16",
        "price": "170 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/oppo/400/300",
        "categorie": "Électronique",
        "date": "01 août 2026",
        "description": "Oppo Reno 16, écran impeccable, batterie excellente.",
    },
    {
        "title": "Yamaha MT-09",
        "price": "2 000 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/mt09/400/300",
        "categorie": "Véhicules",
        "date": "01 août 2026",
        "description": "Yamaha MT-09, faible kilométrage, révisée récemment.",
    },
    {
        "title": "Appartement meublé 3 pièces",
        "price": "450 USD / mois",
        "time": "2 jours",
        "loc": "Gombe, Kinshasa",
        "img": "https://picsum.photos/seed/appart/400/300",
        "categorie": "Immobilier",
        "date": "31 juillet 2026",
        "description": "Appartement meublé, 3 pièces, sécurisé, quartier calme.",
    },
    {
        "title": "Canapé 3 places",
        "price": "120 USD",
        "time": "3 jours",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/canape/400/300",
        "categorie": "Maison & Jardin",
        "date": "30 juillet 2026",
        "description": "Canapé 3 places, tissu beige, très peu utilisé.",
    },
]


def main(page: ft.Page):
    page.title = "AnnoncesApp"
    page.bgcolor = PAPER
    page.padding = 0
    page.window.width = 360
    page.window.height = 844
    page.fonts = {
        "Fraunces": "https://raw.githubusercontent.com/google/fonts/main/ofl/fraunces/Fraunces%5BSOFT%2CWONK%2Copsz%2Cwght%5D.ttf"
    }

    state = {"query": "", "categorie": "Tout", "selected": None}
    favorites = set()
    grid_ref = ft.Ref[ft.GridView]()

    # -------------------------------------------------------------- HEADER
    titre = ft.Text("AnnoncesApp", size=18, weight=ft.FontWeight.BOLD, color=INK)

    logo = ft.Row(
        [
            ft.Container(
                content=ft.Icon(ft.Icons.DIAMOND_OUTLINED, color="white", size=16),
                bgcolor=PRIMARY,
                width=34,
                height=34,
                border_radius=10,
                alignment=ft.Alignment.CENTER,
                shadow=ft.BoxShadow(blur_radius=8, color="#2954E555", offset=ft.Offset(0, 3)),
            ),
            titre,
        ],
        spacing=8,
    )

    search_bar = ft.TextField(
        hint_text="Chercher sur AnnoncesApp...",
        border_radius=30,
        bgcolor=CHIP_BG,
        border_color="transparent",
        focused_border_color=PRIMARY,
        content_padding=ft.Padding.symmetric(horizontal=18, vertical=8),
        height=44,
        expand=True,
        text_size=14,
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: filter_annonces(),
    )

    publish_btn = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, size=16, color="white"),
             ft.Text("Publier une annonce", color="white", size=13, weight=ft.FontWeight.W_600)],
            spacing=6,
            tight=True,
        ),
        bgcolor=PRIMARY,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=24),
            padding=ft.Padding.symmetric(horizontal=18, vertical=16),
            elevation=0,
        ),
    )

    favoris_btn = ft.Column(
        [ft.Icon(ft.Icons.FAVORITE_BORDER, color=INK, size=20), ft.Text("Favoris", size=11, color=INK)],
        spacing=2,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    profil_btn = ft.Column(
        [
            ft.CircleAvatar(content=ft.Icon(ft.Icons.PERSON, color="white", size=16), radius=13, bgcolor=MUTED),
            ft.Text("Marc Lucien", size=11, color=INK),
        ],
        spacing=2,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def on_resize(e):
        wide = page.width and page.width >= 700

        titre.visible = wide
        publish_btn.visible = page.width >= 700
        #publish_btn.content.controls[1].visible = wide

    # Mise à jour du ratio des cartes
        #grid.child_aspect_ratio = 0.25 if wide else 0.26
        page.update()

    page.on_resize = on_resize
    titre.visible = (page.width or 800) >= 700
    publish_btn.visible = (page.width or 800) >= 700
    header = ft.Container(
        padding=ft.Padding.symmetric(horizontal=20, vertical=14),
        bgcolor=CARD_BG,
        border=ft.Border(bottom=ft.BorderSide(1, BORDER)),
        alignment=ft.Alignment.CENTER,
        content=ft.Container(
            width=1100,
            content=ft.Row(
                [
                    logo,
                    ft.Container(expand=True, margin=ft.Margin.symmetric(horizontal=8), content=search_bar),
                    favoris_btn,
                    profil_btn,
                    publish_btn,
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
            ),
        ),
    )

    # ---------------------------------------------------------------- HERO
    hero = ft.Container(
        height=180,
        border_radius=16,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[PRIMARY, PRIMARY_DARK],
        ),
        padding=ft.Padding.symmetric(horizontal=28, vertical=22),
        content=ft.Stack(
            [
                ft.Container(
                    right=-30, top=-30, width=160, height=160, border_radius=80, bgcolor="#FFFFFF14"
                ),
                ft.Container(
                    right=40, bottom=-50, width=100, height=100, border_radius=50, bgcolor="#FFFFFF10"
                ),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Achète facile", size=30, weight=ft.FontWeight.W_600,
                                        font_family="Fraunces", color="white", italic=True),
                                ft.Text("Vends rapide", size=30, weight=ft.FontWeight.W_600,
                                        font_family="Fraunces", color="white", italic=True),
                                ft.Container(height=10),
                                ft.Text("Des milliers d'annonces près de chez vous",
                                        size=13, color="#FFFFFFCC"),
                            ],
                            spacing=0,
                        ),
                        ft.Container(expand=True),
                        ft.Icon(ft.Icons.PHONE_IPHONE, size=90, color="#FFFFFF33"),
                    ],
                ),
            ]
        ),
    )

    # ---------------------------------------------------------- CATÉGORIES
    chip_refs = {}

    def select_categorie(cat):
        state["categorie"] = cat
        for name, ref in chip_refs.items():
            selected = name == cat
            ref.current.bgcolor = PRIMARY if selected else CHIP_BG
            ref.current.content.controls[0].color = "white" if selected else INK
            ref.current.content.controls[1].color = "white" if selected else INK
        filter_annonces()
        page.update()

    def build_chip(name, icon):
        ref = ft.Ref[ft.Container]()
        chip_refs[name] = ref
        is_selected = name == state["categorie"]
        chip = ft.Container(
            ref=ref,
            bgcolor=PRIMARY if is_selected else CHIP_BG,
            border_radius=20,
            padding=ft.Padding.symmetric(horizontal=14, vertical=9),
            on_click=lambda e, n=name: select_categorie(n),
            content=ft.Row(
                [
                    ft.Icon(icon, size=15, color="white" if is_selected else INK),
                    ft.Text(name, size=12.5, weight=ft.FontWeight.W_500, color="white" if is_selected else INK),
                ],
                spacing=6,
                tight=True,
            ),
        )
        return chip

    categorie_row = ft.Row(
        controls=[build_chip(n, i) for n, i in CATEGORIES],
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
    )

    # --------------------------------------------------------- AD BANNER
    ad_banner = ft.Container(
        alignment=ft.Alignment.CENTER,
        content=ft.Container(
            width=1100,
            margin=ft.Margin.symmetric(horizontal=0, vertical=14),
            padding=16,
            border_radius=14,
            bgcolor=CARD_BG,
            border=ft.Border.all(1, BORDER),
            shadow=ft.BoxShadow(blur_radius=10, color="#00000008", offset=ft.Offset(0, 2)),
            content=ft.Column(
                [
                    ft.Text("PUBLICITÉ", size=10.5, color=MUTED, weight=ft.FontWeight.W_600),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Activez votre compte vérifié", size=17,
                                            weight=ft.FontWeight.BOLD, color=INK),
                                    ft.Text("Vendez plus vite avec le badge vérifié", size=12, color=MUTED),
                                ],
                                expand=True,
                                spacing=2,
                            ),
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [ft.Text("Ouvrir", color="white", size=12, weight=ft.FontWeight.W_600),
                                     ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=12, color="white")],
                                    spacing=6, tight=True,
                                ),
                                bgcolor=GOLD,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), elevation=0),
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=8,
            ),
        ),
    )

    # -------------------------------------------------------------- CARDS
    def go_to_detail(item):
        state["selected"] = item
        asyncio.create_task(page.push_route("/details"))

    def listing_card(item):
        is_fav_ref = ft.Ref[ft.IconButton]()

        def toggle_fav(e):
            key = item["title"]
            if key in favorites:
                favorites.discard(key)
                is_fav_ref.current.icon = ft.Icons.FAVORITE_BORDER
                is_fav_ref.current.icon_color = INK
            else:
                favorites.add(key)
                is_fav_ref.current.icon = ft.Icons.FAVORITE
                is_fav_ref.current.icon_color = RUST
            is_fav_ref.current.update()

        price_color = GOLD if "sur demande" in item["price"].lower() else RUST_DARK

        return ft.Container(
            width=220,
            bgcolor=CARD_BG,
            border=ft.Border.all(1, BORDER),
            border_radius=16,
            on_click=lambda e, it=item: go_to_detail(it),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            shadow=ft.BoxShadow(blur_radius=12, color="#00000008", offset=ft.Offset(0, 4)),
            content=ft.Column(
                [
                    ft.Stack(
                        [
                            ft.Image(src=item["img"], height=140, width=220, fit="cover"),
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
                                content=ft.Text(item["categorie"], size=10, color="white", weight=ft.FontWeight.W_600),
                                bgcolor=f"{PRIMARY}CC",
                                border_radius=20,
                                padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                                bottom=8, left=8,
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    ref=is_fav_ref,
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
                        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                        content=ft.Column(
                            [
                                ft.Text(item["price"], size=15, weight=ft.FontWeight.BOLD, color=price_color),
                                ft.Text(
                                    item["title"], size=12.5, color=INK,
                                    max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
                                    weight=ft.FontWeight.W_500,
                                ),
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=13, color=MUTED),
                                        ft.Text(item["loc"], size=11, color=MUTED),
                                    ],
                                    spacing=2,
                                ),
                            ],
                            spacing=5,
                        ),
                    ),
                ],
                spacing=0,
            ),
        )

    grid = ft.GridView(
        ref=grid_ref,
        expand=False,
        max_extent=232,
        child_aspect_ratio=0.72,
        spacing=14,
        run_spacing=14,
        controls=[listing_card(a) for a in ANNONCES],
    )

    section_title = ft.Row(
        [
            ft.Text("Annonces récentes", size=17, weight=ft.FontWeight.BOLD, color=INK),
            ft.Container(expand=True),
            ft.Text(f"{len(ANNONCES)} résultats", size=12, color=MUTED),
        ],
    )

    empty_state = ft.Container(
        visible=False,
        padding=40,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            [
                ft.Icon(ft.Icons.SEARCH_OFF, size=40, color=MUTED),
                ft.Text("Aucune annonce ne correspond à votre recherche", size=13, color=MUTED),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
    )

    def filter_annonces():
        query = (search_bar.value or "").strip().lower()
        cat = state["categorie"]
        filtered = [
            a for a in ANNONCES
            if (cat == "Tout" or a["categorie"] == cat)
            and (query in a["title"].lower() or query in a["loc"].lower())
        ]
        grid.controls = [listing_card(a) for a in filtered]
        empty_state.visible = len(filtered) == 0
        grid.visible = len(filtered) > 0
        section_title.controls[2].value = f"{len(filtered)} résultats"
        page.update()

    long = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=18,
        controls=[hero, categorie_row, ad_banner, section_title, grid, empty_state],
    )

    content_area = ft.Column(
        expand=True,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            header,
            ft.Container(
                alignment=ft.Alignment.TOP_CENTER,
                padding=ft.Padding.symmetric(horizontal=20, vertical=18),
                content=ft.Container(width=1100, content=long),
            ),
        ],
    )

    # --------------------------------------------------------- DETAIL VIEW
    def build_detail_view(annonce):
        back_btn = ft.Row(
            [
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=INK,
                              on_click=lambda e: asyncio.create_task(page.push_route("/"))),
                ft.Text("Retour aux annonces", color=INK, size=13, weight=ft.FontWeight.W_500),
            ],
            spacing=0,
        )

        return ft.Column(
            [
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.symmetric(horizontal=20, vertical=14),
                    content=ft.Container(width=1100, content=back_btn),
                ),
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=ft.Container(
                        width=1100,
                        padding=ft.Padding.symmetric(horizontal=20),
                        content=ft.ResponsiveRow(
                            [
                                ft.Container(
                                    content=ft.Image(
                                        src=annonce["img"], fit="cover", border_radius=16, height=380,
                                    ),
                                    col={"sm": 12, "md": 7},
                                ),
                                ft.Container(
                                    col={"sm": 12, "md": 5},
                                    padding=ft.Padding.only(left=20, top=8),
                                    content=ft.Column(
                                        [
                                            ft.Container(
                                                content=ft.Text(annonce["categorie"], size=12, color="white"),
                                                bgcolor=PRIMARY,
                                                padding=ft.Padding.symmetric(horizontal=10, vertical=5),
                                                border_radius=20,
                                            ),
                                            ft.Text(annonce["title"], size=22, weight=ft.FontWeight.BOLD,
                                                     font_family="Fraunces", color=INK),
                                            ft.Text(annonce["price"], size=26, weight=ft.FontWeight.BOLD,
                                                     color=RUST_DARK),
                                            ft.Row(
                                                [
                                                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=16, color=MUTED),
                                                    ft.Text(annonce["loc"], color=MUTED, size=13),
                                                    ft.Container(width=10),
                                                    ft.Icon(ft.Icons.ACCESS_TIME, size=14, color=MUTED),
                                                    ft.Text(annonce["date"], color=MUTED, size=13),
                                                ],
                                                spacing=4,
                                            ),
                                            ft.Divider(color=BORDER),
                                            ft.Text("Description", weight=ft.FontWeight.W_600, color=INK, size=14),
                                            ft.Text(annonce["description"], color="#5A5A5A", size=13),
                                            ft.Divider(color=BORDER),
                                            ft.Row(
                                                [
                                                    ft.CircleAvatar(
                                                        content=ft.Icon(ft.Icons.PERSON, color="white", size=18),
                                                        radius=18, bgcolor=MUTED,
                                                    ),
                                                    ft.Column(
                                                        [
                                                            ft.Text("Marc Lucien", size=13, weight=ft.FontWeight.W_600, color=INK),
                                                            ft.Text("Vendeur particulier", size=11, color=MUTED),
                                                        ],
                                                        spacing=0,
                                                    ),
                                                ],
                                                spacing=10,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.ElevatedButton(
                                                        content=ft.Row(
                                                            [ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=16, color="white"),
                                                             ft.Text("Contacter le vendeur", color="white",
                                                                     size=13, weight=ft.FontWeight.W_600)],
                                                            spacing=6, tight=True,
                                                        ),
                                                        style=ft.ButtonStyle(
                                                            bgcolor=RUST,
                                                            shape=ft.RoundedRectangleBorder(radius=10),
                                                            padding=ft.Padding.symmetric(horizontal=18, vertical=16),
                                                            elevation=0,
                                                        ),
                                                        expand=True,
                                                    ),
                                                    ft.IconButton(
                                                        icon=ft.Icons.FAVORITE_BORDER, icon_color=INK,
                                                        bgcolor=CHIP_BG, icon_size=20,
                                                    ),
                                                ],
                                                spacing=10,
                                            ),
                                        ],
                                        spacing=10,
                                    ),
                                ),
                            ],
                        ),
                    ),
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def route_change(e=None):
        page.views.clear()
        page.views.append(ft.View(route="/", padding=0, controls=[content_area], bgcolor=PAPER))
        if page.route == "/details":
            annonce = state["selected"] or ANNONCES[0]
            page.views.append(
                ft.View(route="/details", padding=0, controls=[build_detail_view(annonce)], bgcolor=PAPER)
            )

    page.on_route_change = route_change
    route_change()


ft.app(target=main)
