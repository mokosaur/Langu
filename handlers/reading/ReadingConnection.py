import json

from tornado import gen

from handlers.BaseConnection import BaseConnection


class ReadingConnection(BaseConnection):
    """Reading connection implementation"""

    def on_answer(self, answers):
        message = json.loads(answers)
        for a in message:
            if str(self.answers[int(a)]) == message[a]:
                self.score = 100 / len(self.answers)
        self.send(self.score)
        self.add_score()

    def fetch_user_data(self, user):
        self.email = user['email']
        self.level = 3

    @gen.coroutine
    def prepare_dataset(self):
        self.dataset = yield self.db.get_reading('english', self.level)

    def estimate_dataset_params(self):
        title = self.dataset['title']
        text = self.dataset['text']
        questions = self.dataset['questions']
        self.answers = self.dataset['answers']
        return {'title': title, 'text': text, 'questions': questions}

    def send_dataset(self, params):
        self.send(params['title'] + '|' + params['text'])
        self.send(params['questions'])

    @gen.engine
    def add_score(self):
        yield self.db.update_game_score(self.email, 'reading', 'english', self.score * self.level)
