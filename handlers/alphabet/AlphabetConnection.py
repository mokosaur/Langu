import random

from tornado import gen

from handlers.BaseConnection import BaseConnection


class AlphabetConnection(BaseConnection):
    """Alphabet connection implementation"""

    def on_score(self, score):
        self.score = score
        params = self.estimate_dataset_params()
        self.send_dataset(params)
        self.update_score()

    def fetch_user_data(self, user):
        self.email = user['email']
        if 'alphabet' in user and 'greek' in user['alphabet']:
            self.score = user['alphabet']['greek']
        else:
            self.score = 0

    @gen.coroutine
    def prepare_dataset(self):
        self.dataset = (yield self.db.get_alphabet('greek'))['alphabet']

    def estimate_dataset_params(self):
        alphabet_variety = self.dataset[0: min(int(self.score) // 1000 + 5, len(self.dataset))]
        n_letters = min(int(self.score) // 5000 + 5, 16)
        return {'alphabet_variety': alphabet_variety, 'n_letters': n_letters}

    def send_dataset(self, params):
        self.send(random.sample(params['alphabet_variety'], params['n_letters']))

    @gen.engine
    def update_score(self):
        yield self.db.update_game_score(self.email, 'alphabet', 'greek', self.score, False)
