import flet as ft


def lobby_view(page: ft.Page, game, change_screen):
    player_input = ft.TextField(
        label="Name", expand=True, on_submit=lambda e: handle_add_player()
    )

    players_list = ft.ListView(expand=True, spacing=10)

    language_dropdown = ft.Dropdown(
        label="Select Language",
        value="english",
        options=[
            ft.dropdown.Option("english", "English"),
            ft.dropdown.Option("polish", "Polski"),
        ],
        width=300,
    )

    rounds_dropdown = ft.Dropdown(
        label="Words per Game",
        value="15",
        options=[
            ft.dropdown.Option("5", "5 Words"),
            ft.dropdown.Option("10", "10 Words"),
            ft.dropdown.Option("15", "15 Words"),
            ft.dropdown.Option("20", "20 Words"),
            ft.dropdown.Option("all", "All Words"),
        ],
        width=300,
    )

    def render_players():
        players_list.controls.clear()
        for player_name in game.players:
            players_list.controls.append(
                ft.ListTile(
                    title=ft.Text(player_name, size=20),
                    trailing=ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED_400,
                        on_click=lambda e, name=player_name: handle_remove_player(name),
                    ),
                )
            )
        page.update()

    def handle_add_player():
        name = player_input.value.strip()
        if name:
            game.add_player(name)
            player_input.value = ""
            render_players()

    def handle_remove_player(name):
        game.remove_player(name)
        render_players()

    def handle_start_game(e):
        if len(game.players) < 1:
            page.open(ft.SnackBar(ft.Text("Add at least 1 player")))
            return

        game.select_language(language_dropdown.value, rounds_dropdown.value)
        game.new_game()
        change_screen("game")

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "SING THAT WORD",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                language_dropdown,
                rounds_dropdown,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    [
                        player_input,
                        ft.IconButton(
                            icon=ft.Icons.ADD_BOX_ROUNDED,
                            icon_size=45,
                            icon_color=ft.Colors.BLUE_400,
                            on_click=lambda e: handle_add_player(),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(),
                players_list,
                ft.ElevatedButton(
                    "START GAME",
                    on_click=handle_start_game,
                    width=300,
                    height=60,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_700,
                        text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD),
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=30,
        expand=True,
    )
