import flet as ft
import traceback

from views.landing import landing_view
from views.host_lobby import host_lobby_view
from views.client_lobby import client_lobby_view
from views.host_game import host_game_view
from views.client_game import client_game_view
from views.results import results_view

ACTIVE_ROOMS = {}


def main(page: ft.Page):
    try:
        page.title = "Sing That Word"
        page.theme_mode = ft.ThemeMode.DARK
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def change_screen(screen_name, game_instance=None):
            page.clean()

            if screen_name == "landing":
                page.add(landing_view(page, ACTIVE_ROOMS, change_screen))
            elif screen_name == "host_lobby":
                page.add(host_lobby_view(page, game_instance, change_screen))
            elif screen_name == "client_lobby":
                page.add(client_lobby_view(page, game_instance, change_screen))
            elif screen_name == "host_game":
                page.add(host_game_view(page, game_instance, change_screen))
            elif screen_name == "client_game":
                page.add(client_game_view(page, game_instance, change_screen))
            elif screen_name == "results":
                page.add(results_view(page, game_instance, change_screen))

            page.update()

        change_screen("landing")

    except Exception as e:
        page.clean()
        page.add(ft.Text(f"APP CRASHED: {str(e)}", color=ft.Colors.RED_400))
        page.update()
        traceback.print_exc()


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550, host="0.0.0.0")
