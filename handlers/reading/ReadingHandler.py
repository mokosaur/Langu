from handlers.BaseHandler import BaseHandler
from tornado import web


class ReadingHandler(BaseHandler):
    @web.asynchronous
    @web.authenticated
    async def get(self):
        user = self.get_current_user()
        document = await self.db.get_user(user)
        self.render('reading.jade', user=document["email"])
