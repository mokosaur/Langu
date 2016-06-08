from sockjs.tornado import SockJSConnection

from tornado import gen

from DatabaseConnection import DatabaseConnection


class BaseConnection(SockJSConnection):
    """Base connection implementation"""

    def on_open(self, info):
        self.db = DatabaseConnection()

    def on_message(self, message):
        request, body = message.split('|', 1)
        callback = getattr(self, 'on_' + request)
        callback(body)

    @gen.engine
    def on_auth(self, message):
        user = yield self.db.get_user(message)
        self.fetch_user_data(user)
        yield self.prepare_dataset()
        params = self.estimate_dataset_params()
        self.send_dataset(params)

    def on_close(self): pass

    # These methods should be implemented
    def fetch_user_data(self, user): pass
    def prepare_dataset(self): pass
    def estimate_dataset_params(self): pass
    def send_dataset(self, params): pass


