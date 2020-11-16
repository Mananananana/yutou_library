import unittest

from yutou_library import create_app
from yutou_library.extensions import db
from yutou_library.models import User


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app = create_app("testing")
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()

        user = User(email="123456@qq.com", phone="13912345678")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()

    def tearDown(self) -> None:
        db.drop_all()
        self.context.pop()
