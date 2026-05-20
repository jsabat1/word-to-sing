import random
import json

with open("words_eng.json", "r", encoding="utf-8") as f1:
    words_eng = json.load(f1)
with open("words_pol.json", "r", encoding="utf-8") as f2:
    words_pol = json.load(f2)


class GamePlay:
    def __init__(self):
        self.players = {}
        self.word_pool = []
        self.current_word = None

    def select_language(self, language):
        if language == "english":
            self.word_pool = words_eng.copy()
        elif language == "polish":
            self.word_pool = words_pol.copy()
        else:
            raise ValueError("Unsupported language. Choose 'english' or 'polish'.")

        random.shuffle(self.word_pool)

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

        self.draw_next_word()

    def update_score(self, player_name):
        if player_name in self.players:
            self.players[player_name] += 1
