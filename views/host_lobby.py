import flet as ft


def host_lobby_view(page: ft.Page, game, change_screen):
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

    def on_message(topic, message):
        if message["type"] == "player_joined":
            game.add_player(message["name"])

            bonus = message["bonus_word"].strip()
            if bonus and bonus.lower() not in [w.lower() for w in game.word_pool]:
                game.word_pool.append(bonus)

            players_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(message["avatar"], size=40),
                            ft.Text(
                                message["name"], size=25, weight=ft.FontWeight.BOLD
                            ),
                        ]
                    ),
                    bgcolor=ft.Colors.BLUE_900,
                    padding=10,
                    border_radius=10,
                )
            )
            page.update()

    page.pubsub.subscribe_topic(game.room_code, on_message)

    def handle_start(e):
        if len(game.players) < 1:
            snack = ft.SnackBar(ft.Text("Waiting for players to join..."))
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return

        game.select_language(language_dropdown.value, rounds_dropdown.value)
        game.new_game()

        page.pubsub.send_all_on_topic(game.room_code, {"type": "game_started"})
        change_screen("host_game", game_instance=game)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("JOIN AT", size=20, color=ft.Colors.GREY_400),
                ft.Text(
                    f"ROOM CODE: {game.room_code}",
                    size=60,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.AMBER_400,
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                language_dropdown,
                rounds_dropdown,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Text("PLAYERS IN LOBBY:", size=20),
                players_list,
                ft.ElevatedButton(
                    "START GAME",
                    width=300,
                    height=80,
                    on_click=handle_start,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        padding=40,
    )
