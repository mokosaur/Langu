from handlers.BaseHandler import BaseHandler
from tornado import web
import hashlib


class RegistrationHandler(BaseHandler):
    @web.asynchronous
    async def post(self):
        print("Registered")
        email = self.get_argument("email", "")
        name = self.get_argument("name", "")
        password = self.get_argument("password", "")
        document = await self.db.get_user(email)
        if document == None:
            self.db.crete_user(email, name, password)
            self.set_current_user(email)
            self.redirect('/')
        else:
            self.render('login.jade', error="This e-mail address is already used!")
