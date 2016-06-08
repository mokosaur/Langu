from handlers.BaseHandler import BaseHandler
from tornado import web
import hashlib


class LoginHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        self.render('login.jade', error="")

    async def post(self):
        print("Logged")
        email = self.get_argument("email", "")
        password = self.get_argument("password", "")
        document = await self.db.get_user(email)
        # cursor = self.db.users.find()
        # async for d in self.db.users.find():
        #     print(d)
        if document != None and hashlib.sha256(str.encode(password)).hexdigest() == document['password']:
            self.set_current_user(email)
            self.redirect('/')
        else:
            self.render('login.jade', error="Wrong e-mail or password!")
