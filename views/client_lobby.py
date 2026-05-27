import flet as ft


def client_lobby_view(page: ft.Page, game, change_screen):
    name_input = ft.TextField(label="Your Name", text_align=ft.TextAlign.CENTER)
    bonus_word_input = ft.TextField(label="Bonus Word", text_align=ft.TextAlign.CENTER)

    avatar_dropdown = ft.Dropdown(
        label="Pick Avatar",
        value="😎",
        options=[
            ft.dropdown.Option("😎"),
            ft.dropdown.Option("🤠"),
            ft.dropdown.Option("👽"),
            ft.dropdown.Option("👻"),
            ft.dropdown.Option("🤖"),
            ft.dropdown.Option("🦄"),
        ],
    )

    waiting_text = ft.Text(
        "Waiting for Host to start...",
        size=20,
        color=ft.Colors.AMBER_400,
        visible=False,
    )
    join_button = ft.ElevatedButton("JOIN ROOM", height=60, width=200)

    def on_message(topic, message):
        if message["type"] == "game_started":
            change_screen("client_game", game_instance=game)

    page.pubsub.subscribe_topic(game.room_code, on_message)

    def handle_join(e):
        if not name_input.value:
            return

        page.pubsub.send_all_on_topic(
            game.room_code,
            {
                "type": "player_joined",
                "name": name_input.value.strip(),
                "avatar": avatar_dropdown.value,
                "bonus_word": bonus_word_input.value.strip(),
            },
        )

        page.session.store.set("player_name", name_input.value.strip())

        name_input.visible = False
        bonus_word_input.visible = False
        avatar_dropdown.visible = False
        join_button.visible = False
        waiting_text.visible = True
        page.update()

    join_button.on_click = handle_join

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Room: {game.room_code}", size=30, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                name_input,
                avatar_dropdown,
                bonus_word_input,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                join_button,
                waiting_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True,
        padding=30,
    )
