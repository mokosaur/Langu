from handlers.BaseHandler import BaseHandler
from tornado import web


class AlphabetHandler(BaseHandler):
    @web.asynchronous
    @web.authenticated
    async def get(self):
        user = self.get_current_user()
        document = await self.db.get_user(user)
        if 'alphabet' in document and 'greek' in document['alphabet']:
            score = document['alphabet']['greek']
        else:
            score = 0
        self.render('alphabet.jade', user=document["email"], score=score)
