import flet as ft
import traceback
from state import GamePlay

from views.lobby import lobby_view
from views.game import game_view
from views.results import results_view


def main(page: ft.Page):
    try:
        page.title = "Sing That Word"
        page.theme_mode = ft.ThemeMode.DARK

        page.window.width = 400
        page.window.height = 800
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        game = GamePlay()

        # manual router, pierdoli sie ten nowy
        def change_screen(screen_name):
            page.clean()

            if screen_name == "lobby":
                page.add(lobby_view(page, game, change_screen))
            elif screen_name == "game":
                page.add(game_view(page, game, change_screen))
            elif screen_name == "results":
                page.add(results_view(page, game, change_screen))

            page.update()

        change_screen("lobby")

    except Exception as e:
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text(
                        "APP CRASHED:",
                        size=30,
                        color=ft.Colors.RED_400,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(str(e), size=20, color=ft.Colors.AMBER_400),
                    ft.Text("Check your terminal for the full error.", size=16),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()
        print("--- APP CRASHED ---")
        traceback.print_exc()


if __name__ == "__main__":
    ft.run(main)
