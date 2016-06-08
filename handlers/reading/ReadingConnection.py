from sockjs.tornado import SockJSConnection
import json

from tornado import gen

from DatabaseConnection import DatabaseConnection


class ReadingConnection(SockJSConnection):
    """Reading connection implementation"""

    def on_open(self, info):
        self.db = DatabaseConnection()
        self.score = 0

    def on_message(self, message):
        if len(message) > 0 and message[0] == '{':
            message = json.loads(message)
            for a in message:
                if str(self.answers[int(a)]) == message[a]:
                    self.score += 100 / len(self.answers)
            self.send(self.score)
            self.add_score()
        else:
            self.email, self.language, self.level = message.split(',')
            self.level = int(self.level)
            self.get_reading(self.language, self.level, self.send_reading)

    def on_close(self):
        pass

    @gen.engine
    def add_score(self):
        yield self.db.update_game_score(self.email, 'reading', self.language, self.score * self.level)

    @gen.engine
    def get_reading(self, language, level, callback):
        reading = yield self.db.get_reading(language, level)
        self.title = reading['title']
        self.text = reading['text']
        self.questions = reading['questions']
        self.answers = reading['answers']
        callback()

    def send_reading(self):
        self.send(self.title+'|'+self.text)
        self.send(self.questions)



