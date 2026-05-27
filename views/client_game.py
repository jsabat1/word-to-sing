import flet as ft


def client_game_view(page: ft.Page, game, change_screen):
    player_name = page.session.store.get("player_name")

    buzz_btn = ft.ElevatedButton(
        "BUZZ!",
        width=300,
        height=300,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
            shape=ft.CircleBorder(),
            text_style=ft.TextStyle(size=50, weight=ft.FontWeight.BOLD),
        ),
    )

    status_text = ft.Text("Get ready...", size=24)

    def handle_buzz(e):
        page.pubsub.send_all_on_topic(
            game.room_code, {"type": "buzz", "player": player_name}
        )

    buzz_btn.on_click = handle_buzz

    def on_message(topic, message):
        if message["type"] == "lockout":
            if message["winner"] == player_name:
                buzz_btn.style.bgcolor = ft.Colors.GREEN_400
                buzz_btn.text = "SING!"
                status_text.value = "You got it! Sing loud!"
            else:
                buzz_btn.style.bgcolor = ft.Colors.GREY_800
                buzz_btn.text = "LOCKED"
                status_text.value = f"{message['winner']} buzzed first!"

            buzz_btn.disabled = True
            page.update()

        elif message["type"] == "next_word":
            buzz_btn.style.bgcolor = ft.Colors.GREEN_700
            buzz_btn.text = "BUZZ!"
            buzz_btn.disabled = False
            status_text.value = "New word! Get ready..."
            page.update()

        elif message["type"] == "game_over":
            change_screen("results", game_instance=game)

    page.pubsub.subscribe_topic(game.room_code, on_message)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    f"Playing as: {player_name}", size=20, color=ft.Colors.BLUE_400
                ),
                ft.Container(expand=True),
                buzz_btn,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                status_text,
                ft.Container(expand=True),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        padding=20,
    )
