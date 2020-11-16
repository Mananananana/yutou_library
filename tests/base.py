import unittest

from flask import url_for

from yutou_library import create_app
from yutou_library.extensions import db
from yutou_library.models import User


class BaseTestCase(unittest.TestCase):
    def get_token(self):
        response = self.client.post(url_for("api_v1.login"), json={"method": "phone",
                                                                   "phone": '13912345678',
                                                                   "password": "123456"})
        data = response.get_json()
        return data["token"]

    def setUp(self) -> None:
        app = create_app("testing")
        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

        db.create_all()

        user = User(email="123456@qq.com", phone="13912345678", gender="m", name="laichaoqun")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()

    def tearDown(self) -> None:
        db.drop_all()
        self.context.pop()
