import flet as ft


def results_view(page: ft.Page, game):
    sorted_players = sorted(game.players.items(), key=lambda x: x[1], reverse=True)

    leaderboard = ft.Column(spacing=15, expand=True)

    for index, (name, score) in enumerate(sorted_players):
        placement_marker = "winner" if index == 0 else f"#{index + 1}"
        leaderboard.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            f"{placement_marker} {name}",
                            size=22,
                            weight=(
                                ft.FontWeight.BOLD
                                if index == 0
                                else ft.FontWeight.NORMAL
                            ),
                        ),
                        ft.Text(
                            f"{score} pts",
                            size=22,
                            color=(
                                ft.Colors.AMBER_400 if index == 0 else ft.Colors.WHITE
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=10,
                bgcolor=(ft.Colors.WHITE10 if index > 0 else ft.Colors.BLUE_900),
                border_radius=8,
            )
        )

    async def replay_game(e):
        game.new_game()
        await page.push_route("/game")

    return ft.View(
        "/results",
        [
            ft.Text(
                "GAME OVER",
                size=32,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Divider(height=20),
            leaderboard,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            ft.ElevatedButton(
                "PLAY AGAIN",
                on_click=replay_game,
                width=300,
                height=60,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                ),
            ),
            ft.TextButton(
                "MAIN MENU",
                on_click=lambda e: page.push_route("/"),
                width=300,
                height=50,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=30,
    )
