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
SUCCESS = "#5A8F5B"
DANGER = "#C0463A"

COULEUR_PRIMAIRE = "#B5563A"      # rust/orange chaud (utilisé sur le formulaire de publication)
COULEUR_PRIMAIRE_FONCE = "#8C4229"
COULEUR_ACCENT = "#D98E4A"

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
    breakpoints = {
        "phone": 0,
        "tablet": 240,
        "desktop": 800,
    }
    state = {"query": "", "categorie": "Tout", "selected": None}
    favorites = set()

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

    def go_to_publier(e=None):
        asyncio.create_task(page.push_route("/publier"))

    publish_btn = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, size=16, color="white"),
             ft.Text("Publier une annonce", color="white", size=13, weight=ft.FontWeight.W_600)],
            spacing=6,
            tight=True,
        ),
        bgcolor=PRIMARY,
        on_click=go_to_publier,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=24),
            padding=ft.Padding.symmetric(horizontal=18, vertical=16),
            elevation=0,
        ),
    )

    def build_header():
        mobile = (page.width or 360) < 700

        if mobile:
            mobile_publish_btn = ft.Container(
                content=ft.Icon(ft.Icons.ADD, color="white", size=18),
                width=36,
                height=36,
                bgcolor=PRIMARY,
                border_radius=10,
                alignment=ft.Alignment.CENTER,
                tooltip="Publier une annonce",
                on_click=go_to_publier,
            )

            mobile_favoris_btn = ft.Container(
                content=ft.Icon(ft.Icons.FAVORITE_BORDER, color=INK, size=18),
                width=36,
                height=36,
                bgcolor="transparent",
                border=ft.Border.all(1, BORDER),
                border_radius=10,
                alignment=ft.Alignment.CENTER,
                tooltip="Favoris",
            )

            mobile_profil_btn = ft.Container(
                content=ft.CircleAvatar(
                    content=ft.Icon(ft.Icons.PERSON, color="white", size=15),
                    radius=17,
                    bgcolor=MUTED,
                ),
                border=ft.Border.all(1.5, PRIMARY),
                border_radius=20,
                padding=1,
                tooltip="Marc Lucien",
            )

            return ft.Container(
                bgcolor=CARD_BG,
                padding=ft.Padding.only(left=18, right=18, top=16, bottom=14),
                border=ft.Border(bottom=ft.BorderSide(1, BORDER)),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                logo,
                                ft.Container(expand=True),
                                mobile_favoris_btn,
                                mobile_profil_btn,
                                mobile_publish_btn,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        ft.Container(
                            margin=ft.Margin.only(top=14),
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.LOCATION_ON_OUTLINED, size=13, color=MUTED),
                                    ft.Text("Kinshasa, RDC", size=11.5, color=MUTED, weight=ft.FontWeight.W_500),
                                ],
                                spacing=3,
                            ),
                        ),
                        ft.Container(
                            margin=ft.Margin.only(top=8),
                            content=search_bar,
                        ),
                    ],
                    spacing=0,
                ),
            )

        desktop_favoris_btn = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.FAVORITE_BORDER, color=INK, size=17),
                    ft.Text("Favoris", size=12.5, color=INK, weight=ft.FontWeight.W_500),
                ],
                spacing=6,
                tight=True,
            ),
            padding=ft.Padding.symmetric(horizontal=12, vertical=9),
            border=ft.Border.all(1, BORDER),
            border_radius=10,
            tooltip="Vos annonces favorites",
        )

        desktop_profil_btn = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.CircleAvatar(
                            content=ft.Icon(ft.Icons.PERSON, color="white", size=14),
                            radius=14,
                            bgcolor=MUTED,
                        ),
                        border=ft.Border.all(1.5, PRIMARY),
                        border_radius=17,
                        padding=1,
                    ),
                    ft.Text("Marc Lucien", size=12.5, color=INK, weight=ft.FontWeight.W_500),
                ],
                spacing=8,
                tight=True,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            border_radius=10,
        )

        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
            bgcolor=CARD_BG,
            border=ft.Border(bottom=ft.BorderSide(1, BORDER)),
            alignment=ft.Alignment.CENTER,
            content=ft.Container(
                width=1160,
                content=ft.Row(
                    [
                        logo,
                        ft.Container(width=32),
                        ft.Container(expand=True, content=search_bar),
                        ft.Container(width=8),
                        desktop_favoris_btn,
                        desktop_profil_btn,
                        publish_btn,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
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

    grid = ft.ResponsiveRow(
        breakpoints=breakpoints,
        columns={"phone": 4, "tablet": 8, "desktop": 12},
        spacing=10,
        run_spacing=10,
        controls=[
            ft.Container(
                content=listing_card(a),
                alignment=ft.Alignment.CENTER,
                col={"phone": 4, "tablet": 4, "desktop": 3},
            )
            for a in ANNONCES
        ],
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
        grid.controls = [
            ft.Container(
                content=listing_card(a),
                alignment=ft.Alignment.CENTER,
                col={"phone": 4, "tablet": 4, "desktop": 3},
            )
            for a in filtered
        ]
        empty_state.visible = len(filtered) == 0
        grid.visible = len(filtered) > 0
        section_title.controls[2].value = f"{len(filtered)} résultats"
        page.update()

    long_column = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=18,
        controls=[hero, categorie_row, ad_banner, section_title, grid, empty_state],
    )

    def build_home_view():
        """Reconstruit la page d'accueil (header inclus) — appelée à chaque
        route_change et à chaque resize, pour que le header bascule bien
        entre les versions mobile / desktop."""
        return ft.Column(
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                build_header(),
                ft.Container(
                    alignment=ft.Alignment.TOP_CENTER,
                    padding=ft.Padding.symmetric(horizontal=20, vertical=18),
                    content=ft.Container(width=1100, content=long_column),
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

    def section_titre(texte):
        return ft.Text(texte, size=16, weight=ft.FontWeight.BOLD, color=INK)

    def carte_conteneur(controls_list):
        return ft.Container(
            margin=ft.Margin.symmetric(horizontal=16, vertical=8),
            padding=20,
            border_radius=18,
            bgcolor=CARD_BG,
            border=ft.Border.all(1, BORDER),
            shadow=ft.BoxShadow(blur_radius=10, color="#00000008", offset=ft.Offset(0, 2)),
            content=ft.Column(spacing=14, controls=controls_list),
        )

    def champ_texte(label, hint=None, icon=None, **kwargs):
        return ft.TextField(
            label=label,
            hint_text=hint,
            prefix_icon=icon,
            border_radius=12,
            filled=True,
            fill_color=CHIP_BG,
            border_color="transparent",
            focused_border_color=PRIMARY,
            label_style=ft.TextStyle(color=MUTED),
            color=INK,
            **kwargs,
        )

    # --------------------------------------------------------- PUBLIER VIEW
    def build_publier_view():
        titre_champ = champ_texte("Titre de l'annonce", hint="Ex: iPhone 15 Pro Max 256 Go", icon=ft.Icons.TITLE)
        prix_champ = champ_texte("Prix", icon=ft.Icons.EURO, keyboard_type=ft.KeyboardType.NUMBER)
        description_champ = champ_texte(
                    None, hint="Décrivez votre article en détail...",
                    multiline=True, min_lines=6, max_lines=10,
                )
        async def handle_get_directory_path(e: ft.Event[ft.Button]):
            files = await ft.FilePicker().pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"]
            )

            if files:
               selected_image.src = files[0].path
               selected_image.visible = True
               icone_ajout_photo.visible = False
               page.update()
        def build_info():
            mobile = (page.width or 360) < 700
            if mobile:
                return ft.Container(
                    bgcolor=CARD_BG,
                    padding=ft.Padding.only(left=18, right=18, top=16, bottom=14),
                    border=ft.Border(bottom=ft.BorderSide(1, BORDER)),
                    content=ft.Column(
                        [
                            titre_champ,
                            ft.Text(""),
                            prix_champ,
                        ],
                        spacing=0,
                    ),
                )
            return ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            titre_champ,
                            ft.Text("Choisissez un titre court et précis. Ne mentionnez pas le prix !"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            prix_champ,
                            ft.Text("Indiquez le prix exact de l'article. Une annonce sans prix aura moins de vue."),
                        ]
                    ),
                ]
            )

        info = build_info()
        def build_description():
            mobile = (page.width or 360) < 700
            if mobile:
                return ft.Container(
                            bgcolor=CARD_BG,
                            padding=ft.Padding.only(left=18, right=18, top=16, bottom=14),
                            border=ft.Border(bottom=ft.BorderSide(1, BORDER)),
                            content=ft.Column(
                                [
                                    description_champ,
                                ],
                                spacing=0,
                            ),
                        )
            return ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    description_champ,
                                    ft.Text("Donnez une description détaillée de votre article. N’indiquez pas vos coordonnées (e-mail, téléphones, …) \n dans la description. "),
                                ]
                            ),
                        ]
                    )
        description = build_description()
        categorie_champ = ft.Dropdown(
            label="Catégorie",
            border_radius=12,
            filled=True,
            fill_color=CHIP_BG,
            border_color="transparent",
            focused_border_color=PRIMARY,
            label_style=ft.TextStyle(color=MUTED),
            color=INK,
            options=[
                ft.dropdown.Option("Immobilier"),
                ft.dropdown.Option("Véhicules"),
                ft.dropdown.Option("Électronique"),
                ft.dropdown.Option("Maison & Jardin"),
                ft.dropdown.Option("Mode & Beauté"),
            ],
        )
        ville_champ = champ_texte("Ville", icon=ft.Icons.LOCATION_ON_OUTLINED)
        

        erreur_texte = ft.Text("", color=DANGER, size=12.5, visible=False)

        selected_image = ft.Image(src="https://picsum.photos/seed/nike/400/300", width=200, height=200, fit="cover",
                                    border_radius=12, visible=False)
        icone_ajout_photo = ft.Icon(ft.Icons.ADD_PHOTO_ALTERNATE_OUTLINED, size=48, color=COULEUR_PRIMAIRE)
        image_path_state = {"src": None}

        
        public = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    padding=ft.Padding.only(top=20, left=20, right=20, bottom=6),
                    content=ft.Column(
                        [
                            ft.Text("Publier une annonce", size=26, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Remplissez les informations ci-dessous pour publier votre annonce.",
                                size=13,
                            ),
                        ],
                        spacing=4,
                    ),
                ),
                carte_conteneur([
                    ft.Container(
                        border=ft.Border.all(2, ft.Colors.with_opacity(0.15, COULEUR_PRIMAIRE)),
                        border_radius=14,
                        padding=24,
                        #on_click=choisir_image,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=6,
                            controls=[
                                icone_ajout_photo,
                                selected_image,
                                ft.Container(height=6),
                                ft.Button(
                                    content="Choisir une photo",
                                    icon=ft.Icons.FOLDER_OPEN,
                                    on_click=handle_get_directory_path,
                                ),
                            ],
                        ),
                    ),
                ]),
                carte_conteneur([
                    section_titre("Informations générales"),
                    info,
                    categorie_champ,
                    ville_champ,
                ]),
                carte_conteneur([
                    section_titre("Description"),
                    description,
                ]),
                ft.Container(
                    margin=ft.Margin.symmetric(horizontal=16, vertical=4),
                    padding=16,
                    border_radius=16,
                    bgcolor=f"{GOLD}26",
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color=GOLD),
                            ft.Text(
                                "Ajoutez une photo et une description détaillée pour vendre plus rapidement.",
                                color=INK,
                                expand=True,
                                size=13,
                            ),
                        ]
                    ),
                ),
                ft.Container(
                    margin=ft.Margin.symmetric(horizontal=16, vertical=4),
                    content=erreur_texte,
                ),
                ft.Container(
                    margin=ft.Margin.symmetric(horizontal=16, vertical=8),
                    content=ft.ElevatedButton(
                        "Publier l'annonce",
                        icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                        style=ft.ButtonStyle(
                            bgcolor=COULEUR_PRIMAIRE,
                            color="white",
                            shape=ft.RoundedRectangleBorder(radius=12),
                        ),
                        expand=True,
                        height=52,
                    ),
                ),
                ft.Container(height=20),
            ],
        )
        return ft.Column(
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    alignment=ft.Alignment.TOP_CENTER,
                    padding=ft.Padding.symmetric(horizontal=20, vertical=18),
                    content=ft.Container(width=1100, content=public),
                ),
            ],
        )
    # ------------------------------------------------------------- ROUTING
    def route_change(e=None):
        page.views.clear()
        page.views.append(ft.View(route="/", padding=0, controls=[build_home_view()], bgcolor=PAPER))
        if page.route == "/details":
            annonce = state["selected"] or ANNONCES[0]
            page.views.append(
                ft.View(route="/details", padding=0, controls=[build_detail_view(annonce)], bgcolor=PAPER)
            )
        if page.route == "/publier":
            page.views.append(
                ft.View(route="/publier", padding=0, controls=[build_publier_view()], bgcolor=PAPER)
            )
        page.update()

    def on_resize(e):
        # Un seul point d'entrée pour le resize : on redessine la vue
        # actuelle (accueil, détail ou publication) selon la largeur.
        route_change()

    page.on_route_change = route_change
    page.on_resize = on_resize
    route_change()
ft.app(target=main)
