from unittest.mock import Mock, patch
import unittest

from tornado.web import Application

from handlers.BaseConnection import BaseConnection
from handlers.BaseHandler import BaseHandler


class TestBaseHandler(unittest.TestCase):
    def setUp(self):
        self.cookie = 'cookie ;3'
        self.request = Mock()
        self.application = Application([('/', BaseHandler)],
                                       cookie_secret=self.cookie, db=Mock())

    def test_single_database_connection(self):
        handler = BaseHandler(self.application, self.request)
        db = handler.db
        self.assertIsNotNone(db)

        handler = BaseHandler(self.application, self.request)
        new_db = handler.db
        self.assertIsNotNone(db)
        self.assertEqual(db, new_db)

    def test_user_cookie(self):
        with patch.object(BaseHandler, 'get_secure_cookie') as m:
            m.return_value = '"success"'
            handler = BaseHandler(self.application, self.request)
            user = handler.get_current_user()
        self.assertEqual('success', user)

    def test_user_cookie_when_none(self):
        with patch.object(BaseHandler, 'get_secure_cookie') as m:
            m.return_value = None
            handler = BaseHandler(self.application, self.request)
            user = handler.get_current_user()
        self.assertIsNone(user)


class TestBaseConnection(unittest.TestCase):
    class Connection(BaseConnection):
        def on_req(self, body):
            pass

    def test_message_parsing(self):
        with patch.object(self.Connection, 'on_req') as mock_method:
            conn = self.Connection(None)
            conn.on_message('req|hello')
        mock_method.assert_called_once_with('hello')


    def test_message_parsing_empty_body(self):
        with patch.object(self.Connection, 'on_req') as mock_method:
            conn = self.Connection(None)
            conn.on_message('req')
        mock_method.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
