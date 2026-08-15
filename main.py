import flet as ft
import asyncio

PRIMARY = "#2954E5"
TEXT_DARK = "#1B1B1F"

RUST = "#E85D42"
PAPER = "#FAF6F1"
INK = "#2B2320"
MUTED = "#8A7F78"
GOLD = "#E8A93C"
CARD_BG = "#FFFFFF"
BORDER = "#EFE7E0"

PRIMARY = "#2954E5"  # bleu du logo / bouton
PRIMARY_DARK = "#1E3FBF"
BG = "#F3F1EE"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#1B1B1F"
TEXT_MUTED = "#6B6B70"
BORDER = "#E4E1DC"

TEXT_DARK = "#2b2b3a"
TEXT_GREY = "#7a7a8c"

RUST = "#E85D42"
RUST_DARK = "#C94A32"
PAPER = "#FAF6F1"
INK = "#2B2320"
MUTED = "#8A7F78"
GOLD = "#E8A93C"
CARD_BG = "#FFFFFF"
BORDER = "#EFE7E0"
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
        "title": "Toyota rav4 2018",
        "price": "16 500 USD",
        "time": "16 heures",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/rav4/400/300",
        "categorie": "Mode & Beauté",
        "date": "01 août 2026",
        "description": "Nike Air Force One first quality, taille unique, jamais portées.",
    },
    {
        "title": "ASUS Rog",
        "price": "200 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/asus/400/300",
        "categorie": "Mode & Beauté",
        "date": "01 août 2026",
        "description": "Nike Air Force One first quality, taille unique, jamais portées.",
    },
    {
        "title": "Oppo Reno 16",
        "price": "170 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/oppo/400/300",
        "categorie": "Mode & Beauté",
        "date": "01 août 2026",
        "description": "Nike Air Force One first quality, taille unique, jamais portées.",
    },
    {
        "title": "Yamaha MT-09",
        "price": "2 000 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/mt09/400/300",
        "categorie": "Mode & Beauté",
        "date": "01 août 2026",
        "description": "Nike Air Force One first quality, taille unique, jamais portées.",
    },
    {
        "title": "Yamaha MT-09",
        "price": "2 000 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/mt09/400/300",
        "categorie": "Mode & Beauté",
        "date": "01 août 2026",
        "description": "Nike Air Force One first quality, taille unique, jamais portées.",
    },
    {
        "title": "Yamaha MT-09",
        "price": "2 000 USD",
        "time": "1 jour",
        "loc": "Kinshasa, RDC",
        "img": "https://picsum.photos/seed/mt09/400/300",
        "categorie": "Mode & Beauté",
        "date": "01 août 2026",
        "description": "Nike Air Force One first quality, taille unique, jamais portées.",
    },
]
def main(page: ft.Page):
    page.title = "Responsive Header"
    page.bgcolor = BG
    page.padding = 0
    page.window.width = 360
    page.window.height = 844
    page.bgcolor = PAPER
    state = {"query": "", "categorie": "Tout", "selected": None}
    favorites = set()
    titre = ft.Text(
        "AnnoncesApp",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=TEXT_DARK,
    )

    logo = ft.Row(
        [
            ft.Container(
                content=ft.Icon(
                    ft.Icons.DIAMOND_OUTLINED,
                    color="white",
                    size=16,
                ),
                bgcolor=PRIMARY,
                width=30,
                height=30,
                border_radius=8,
                alignment=ft.Alignment.CENTER,
            ),
            titre,
        ],
        spacing=8,
    )
    search_bar = ft.TextField(
        hint_text="Chercher sur Annonces...",
        border_radius=30,
        bgcolor="#F3EEE9",
        border_color="transparent",
        #focused_border_color=RUST,
        content_padding=ft.Padding.symmetric(horizontal=18, vertical=8),
        height=42,
        expand=True,
        suffix_icon=ft.Icons.SEARCH,
        #on_submit=lambda e: show_list(search_field.value),
    )
    publish_btn = ft.ElevatedButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.ADD, size=16, color="white"), ft.Text("Publier une annonce", color="white", size=13, weight=ft.FontWeight.W_600)],
                spacing=6,
                tight=True,
                ),
                bgcolor=PRIMARY,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=24), padding=ft.Padding.symmetric(horizontal=16, vertical=14)),
        )
    favoris_btn = ft.Column(
            [ft.Icon(ft.Icons.FAVORITE_BORDER, color=TEXT_DARK, size=20), ft.Text("Favoris", size=11, color=TEXT_DARK)],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    profil_btn = ft.Column(
            [
                ft.CircleAvatar(content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=16), radius=13, bgcolor=TEXT_GREY),
                ft.Text("Marc Lucien", size=11, color=TEXT_DARK),
            ],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    def on_resize(e):
        titre.visible = page.width >= 700
        publish_btn.visible = page.width >= 700
        page.update()

    page.on_resize = on_resize

    # État initial
    titre.visible = (page.width or 800) >= 700
    publish_btn.visible = (page.width or 800) >= 700
    header = ft.Container( 
        padding=20, 
        bgcolor=CARD_BG, 
        border=ft.Border(
            bottom=ft.BorderSide(1, BORDER)), 
            alignment=ft.Alignment.CENTER, 
            content=ft.Container( 
                width=1000, 
                content=ft.Row( 
                    [ logo, 
                     ft.Container( 
                        expand=True, 
                        margin=ft.Margin.symmetric(horizontal=1), 
                        content=search_bar, ), 
                        favoris_btn, 
                        profil_btn, 
                        publish_btn, 
                    ], 
                    alignment=ft.MainAxisAlignment.START, 
                    vertical_alignment=ft.CrossAxisAlignment.CENTER, 
                    spacing=12, 
                    ), 
                    ), 
                    )
    ad_banner = ft.Container(
    alignment=ft.Alignment.CENTER,
    content=ft.Container(
        width=1000,
        margin=ft.Margin.symmetric(horizontal=16, vertical=14),
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
    ),
)
    hero = ft.Container(
            height=170,
            border_radius=12,
            bgcolor=PRIMARY,
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
                            padding=10,
                            content=ft.Column(
                                [
                                    ft.Text(
                                        item["price"],
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=price_color,
                                    ),
                                    ft.Text(
                                        item["title"],
                                        size=12,
                                        color=INK,
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Icon(
                                                ft.Icons.LOCATION_ON_OUTLINED,
                                                size=13,
                                                color=MUTED,
                                            ),
                                            ft.Text(
                                                item["loc"],
                                                size=11,
                                                color=MUTED,
                                            ),
                                        ]
                                    ),
                                ],
                                spacing=4,
                            ),
                        ),
                    ],
                    spacing=0,
                ),
            )
    grid = ft.GridView(
    expand=False,
    max_extent=230,
    child_aspect_ratio=0.67,#0.72,
    spacing=12,
    run_spacing=12,
    controls=[listing_card(a) for a in ANNONCES],
)

    long = ft.Column(
    expand=True,
    scroll=ft.ScrollMode.AUTO,
    spacing=0,
    controls=[
        hero,
        ad_banner,
        grid,
    ],
)   
    content_area= ft.Column(
            expand=True,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                header,
                ft.Divider(),
                ft.Container(
                    alignment=ft.Alignment.TOP_CENTER,
                    padding=20,
                    content=ft.Container(
                        width=1000,
                        content=long,
                    ),
                ),
            ],
        )
    def build_detail_view(annonce):
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
    def route_change(e=None):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                padding = 0,
                controls=[content_area],
                bgcolor=PAPER,
                )
            )
        if page.route == "/details":
            annonce = state["selected"] or ANNONCES[0]
            page.views.append(
                ft.View(
                    route="/details",
                    padding = 0,
                    controls=[build_detail_view(annonce)],
                    bgcolor=PAPER,
                    )
                )
    page.on_route_change = route_change
    route_change()
ft.app(target=main)
