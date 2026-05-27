import flet as ft


def host_game_view(page: ft.Page, game, change_screen):
    word_text = ft.Text(game.current_word, size=80, weight=ft.FontWeight.BOLD)
    status_text = ft.Text(
        "Waiting for someone to buzz...", size=20, color=ft.Colors.GREY_400
    )

    skip_btn = ft.TextButton("SKIP WORD", height=50, visible=True)
    correct_btn = ft.ElevatedButton(
        "NAILED IT! (+1)",
        bgcolor=ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
        visible=False,
        height=60,
    )
    wrong_btn = ft.ElevatedButton(
        "FAILED (-1)",
        bgcolor=ft.Colors.RED_700,
        color=ft.Colors.WHITE,
        visible=False,
        height=60,
    )

    def progress_game():
        if game.draw_next_word():
            word_text.value = game.current_word
            status_text.value = "Waiting for someone to buzz..."
            status_text.color = ft.Colors.GREY_400

            correct_btn.visible = False
            wrong_btn.visible = False
            skip_btn.visible = True

            page.update()
            page.pubsub.send_all_on_topic(game.room_code, {"type": "next_word"})
        else:
            page.pubsub.send_all_on_topic(game.room_code, {"type": "game_over"})
            change_screen("results", game_instance=game)

    def handle_score(points):
        game.update_score(game.buzzed_player, points)
        game.is_locked = False
        game.buzzed_player = None
        progress_game()

    def handle_skip(e):
        progress_game()

    correct_btn.on_click = lambda e: handle_score(1)
    wrong_btn.on_click = lambda e: handle_score(-1)
    skip_btn.on_click = handle_skip

    def on_message(topic, message):
        if message["type"] == "buzz" and not game.is_locked:
            game.is_locked = True
            game.buzzed_player = message["player"]

            status_text.value = f"🎤 {message['player']} is singing!"
            status_text.color = ft.Colors.AMBER_400

            correct_btn.visible = True
            wrong_btn.visible = True
            skip_btn.visible = False

            page.update()

            page.pubsub.send_all_on_topic(
                game.room_code, {"type": "lockout", "winner": message["player"]}
            )

    page.pubsub.subscribe_topic(game.room_code, on_message)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Room: {game.room_code}", size=20, color=ft.Colors.BLUE_400),
                ft.Container(expand=True),
                word_text,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                status_text,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    [wrong_btn, correct_btn],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                skip_btn,
                ft.Container(expand=True),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        padding=20,
    )
