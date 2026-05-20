import random
import json

with open("words_eng.json", "r", encoding="utf-8") as f1:
    words_eng = json.load(f1)
with open("words_pl.json", "r", encoding="utf-8") as f2:
    words_pl = json.load(f2)


class GamePlay:
    def __init__(self):
        self.players = {}
        self.word_pool = []
        self.current_word = None
        self.current_lang = "english"
        self.current_limit = "all"

    def select_language(self, language, limit="all"):
        self.current_lang = language
        self.current_limit = limit
        if language not in ["english", "polish"]:
            raise ValueError("Unsupported language.")
        self.refill_pool()

    def refill_pool(self):
        if self.current_lang == "english":
            self.word_pool = words_eng.copy()
        elif self.current_lang == "polish":
            self.word_pool = words_pl.copy()

        random.shuffle(self.word_pool)

        if self.current_limit != "all":
            self.word_pool = self.word_pool[: int(self.current_limit)]

    def add_player(self, player_name):
        if player_name and player_name not in self.players:
            self.players[player_name] = 0

    def remove_player(self, player_name):
        if player_name in self.players:
            del self.players[player_name]

    def draw_next_word(self):
        if len(self.word_pool) > 0:
            self.current_word = self.word_pool.pop()
            return True
        return False

    def new_game(self):
        for player in self.players:
            self.players[player] = 0

        self.refill_pool()
        self.draw_next_word()

    def update_score(self, player_name):
        if player_name in self.players:
            self.players[player_name] += 1
