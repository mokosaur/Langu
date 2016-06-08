from tornado import web, escape


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = self.settings['db']
        return self._db

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return escape.json_decode(user_json)
        else:
            return None

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", escape.json_encode(user))
        else:
            self.clear_cookie("user")
