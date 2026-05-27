import flet as ft
import random
import string
from state import GamePlay


def landing_view(page: ft.Page, active_rooms, change_screen):

    room_code_input = ft.TextField(
        label="Enter 4-Letter Code",
        width=200,
        text_align=ft.TextAlign.CENTER,
        capitalization=ft.TextCapitalization.CHARACTERS,
        max_length=4,
    )

    def handle_host(e):
        new_code = "".join(random.choices(string.ascii_uppercase, k=4))

        new_game = GamePlay(room_code=new_code, host_session_id=page.session.id)
        active_rooms[new_code] = new_game
        change_screen("host_lobby", game_instance=new_game)

    def handle_join(e):
        code = room_code_input.value.strip().upper()
        if code in active_rooms:
            change_screen("client_lobby", game_instance=active_rooms[code])
        else:
            snack = ft.SnackBar(ft.Text("Room not found!"))
            page.overlay.append(snack)
            snack.open = True
            page.update()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("SING THAT WORD", size=40, weight=ft.FontWeight.BOLD),
                ft.Text("Party Edition", size=20, color=ft.Colors.BLUE_400),
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                ft.ElevatedButton(
                    "HOST NEW GAME",
                    width=300,
                    height=80,
                    on_click=handle_host,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
                    ),
                ),
                ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
                ft.Text("OR JOIN A GAME", size=16, color=ft.Colors.GREY_400),
                ft.Row(
                    [
                        room_code_input,
                        ft.ElevatedButton("JOIN", height=60, on_click=handle_join),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True,
        alignment=ft.Alignment(0, 0),
    )
