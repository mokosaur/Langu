import os

from tornado import ioloop, web
from sockjs.tornado import SockJSRouter
from pyjade.ext.tornado import patch_tornado
import random, string
import logging

from DatabaseConnection import DatabaseConnection
from handlers.IndexHandler import IndexHandler
from handlers.alphabet.AlphabetConnection import AlphabetConnection
from handlers.alphabet.AlphabetHandler import AlphabetHandler
from handlers.authentication.LoginHandler import LoginHandler
from handlers.authentication.LogoutHandler import LogoutHandler
from handlers.authentication.RegistrationHandler import RegistrationHandler
from handlers.reading.ReadingConnection import ReadingConnection
from handlers.reading.ReadingHandler import ReadingHandler

patch_tornado()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    AlphabetRouter = SockJSRouter(AlphabetConnection, '/alphabet')
    ReadingRouter = SockJSRouter(ReadingConnection, '/reading')

    db = DatabaseConnection()

    app = web.Application(
        [
            (r'/', IndexHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/register', RegistrationHandler),
            (r'/alphabet', AlphabetHandler),
            (r'/reading', ReadingHandler),
        ] + AlphabetRouter.urls + ReadingRouter.urls,
        cookie_secret=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64)),
        db=db,
        template_path="templates",
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        login_url='/login'
    )

    app.listen(8080)
    ioloop.IOLoop.current().start()
