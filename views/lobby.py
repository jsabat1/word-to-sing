import flet as ft


def lobby_view(page: ft.Page, game):
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

    async def render_players():
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
        await page.update_async()

    async def handle_add_player():
        name = player_input.value.strip()
        if name:
            game.add_player(name)
            player_input.value = ""
            await render_players()

    async def handle_remove_player(name):
        game.remove_player(name)
        await render_players()

    async def handle_start_game(e):
        if len(game.players) < 1:
            page.open(ft.SnackBar(ft.Text("Add at least 1 player")))
            return

        game.select_language(language_dropdown.value)
        game.new_game()
        await page.push_route("/game")

    return ft.View(
        "/",
        [
            ft.Text(
                "SING THAT WORD",
                size=36,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            language_dropdown,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
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
        padding=30,
    )
