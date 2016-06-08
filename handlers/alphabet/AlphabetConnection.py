from sockjs.tornado import SockJSConnection
import random

from tornado import gen

from DatabaseConnection import DatabaseConnection


class AlphabetConnection(SockJSConnection):
    """Alphabet connection implementation"""

    def on_open(self, info):
        # Send that someone joined
        self.db = DatabaseConnection()
        self.get_alphabet()

    def on_message(self, message):
        # Broadcast message
        if message.isdigit():
            print("message " + message)
            self.score = message
            alph = self.choose_alphabet_subset()
            self.send(alph)
            self.update_score()
        else:
            self.email = message
            self.check_player_score()

    def on_close(self):
        pass

    def choose_alphabet_subset(self):
        alph = self.alphabet[0 : min(int(self.score)//1000 + 5, len(self.alphabet))]
        num = min(int(self.score)//5000 + 5, 16)
        return random.sample(alph, num)

    @gen.engine
    def check_player_score(self):
        player = yield self.db.get_user(self.email)
        if 'alphabet' in player and 'greek' in player['alphabet']:
            self.score = player['alphabet']['greek']
        else:
            self.score = 0
        alph = self.choose_alphabet_subset()
        self.send(alph)

    @gen.engine
    def update_score(self):
        yield self.db.update_game_score(self.email, 'alphabet', 'greek', self.score, False)

    @gen.engine
    def get_alphabet(self):
        self.alphabet = yield self.db.get_alphabet('greek')
        self.alphabet = self.alphabet['alphabet']