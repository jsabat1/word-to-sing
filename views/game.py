import flet as ft


def game_view(page: ft.Page, game, change_screen):
    word_text = ft.Text(
        game.current_word,
        size=55,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    counter_text = ft.Text(
        f"Words remaining: {len(game.word_pool)}", size=16, color=ft.Colors.GREY_400
    )

    def progress_game():
        if game.draw_next_word():
            word_text.value = game.current_word
            counter_text.value = f"Words remaining: {len(game.word_pool)}"
            page.update()
        else:
            change_screen("results")

    def handle_score_selection(player_name):
        game.update_score(player_name)
        score_sheet.open = False
        page.update()
        progress_game()

    player_buttons = []
    for name in game.players:
        player_buttons.append(
            ft.ElevatedButton(
                name,
                width=250,
                height=50,
                on_click=lambda e, player=name: handle_score_selection(player),
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(size=18, weight=ft.FontWeight.W_500)
                ),
            )
        )

    score_sheet = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Who sang it??",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    *player_buttons,
                ],
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=25,
            bgcolor=ft.Colors.GREY_900,
        )
    )

    page.overlay.append(score_sheet)

    def open_scoring(e):
        score_sheet.open = True
        page.update()

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        counter_text,
                        ft.IconButton(
                            icon=ft.Icons.CANCEL_ROUNDED,
                            icon_color=ft.Colors.RED_400,
                            on_click=lambda e: change_screen("lobby"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(expand=True),
                word_text,
                ft.Container(expand=True),
                ft.Row(
                    [
                        ft.TextButton(
                            "PASS",
                            on_click=lambda e: progress_game(),
                            height=60,
                            expand=1,
                        ),
                        ft.ElevatedButton(
                            "GUESSED IT!",
                            on_click=open_scoring,
                            height=60,
                            expand=2,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREEN_700,
                                color=ft.Colors.WHITE,
                                text_style=ft.TextStyle(
                                    size=16, weight=ft.FontWeight.BOLD
                                ),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        expand=True,
    )
