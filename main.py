import flet as ft
import traceback
from state import GamePlay

from views.lobby import lobby_view
from views.game import game_view
from views.results import results_view


async def main(page: ft.Page):
    try:
        page.title = "Sing That Word"
        page.theme_mode = ft.ThemeMode.DARK

        page.window.width = 400
        page.window.height = 800
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        game = GamePlay()

        async def route_change(e):
            page.views.clear()
            route = e.route if e and hasattr(e, "route") else "/"

            if route == "/game":
                page.views.append(game_view(page, game))
            elif route == "/results":
                page.views.append(results_view(page, game))
            else:
                page.views.append(lobby_view(page, game))

            await page.update_async()

        async def view_pop(e):
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop

        await page.push_route("/")

    except Exception as e:
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
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
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        await page.update_async()
        print("--- APP CRASHED ---")
        traceback.print_exc()


if __name__ == "__main__":
    ft.run(main)
