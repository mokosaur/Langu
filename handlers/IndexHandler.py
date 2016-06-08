from handlers.BaseHandler import BaseHandler
from tornado import web


class IndexHandler(BaseHandler):
    @web.asynchronous
    @web.authenticated
    async def get(self):
        user = self.get_current_user()
        document = await self.db.get_user(user)
        alphabet_scores = {}
        reading_scores = {}
        if 'alphabet' in document:
            alphabet_scores = document['alphabet']
        if 'reading' in document:
            reading_scores = document['reading']
        self.render('page.jade', user=document["name"], alphabet_scores=alphabet_scores, reading_scores=reading_scores)
