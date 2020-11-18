import unittest

from flask import url_for

from .base import BaseTestCase
from yutou_library.apis.v1.auth import auth_required, select_library, can
from yutou_library.models import User, Library
from yutou_library.extensions import db


class AuthTestCase(BaseTestCase):
    def test_auth_required(self):
        @self.app.route("/testing")
        @auth_required
        def func():
            return "hello world"
        response = self.client.get(url_for("func"))
        self.assertEqual(response.status_code, 400)
        token = self.get_token()

        response = self.client.get(url_for("func"), headers=[("Authorization", token)])
        self.assertEqual(response.status_code, 400)

        response = self.client.get(url_for("func"), headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"hello world" in response.data)

        response = self.client.get(url_for("func"), headers=[("Authorization", "Bearer ")])
        self.assertEqual(response.status_code, 400)

        token = token[:-1]
        response = self.client.get(url_for("func"), headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 401)

    def test_select_library(self):
        @self.app.route("/testing")
        @auth_required
        @select_library
        def func():
            return "hello world"
        token = self.get_token()
        response = self.client.get(url_for('func'), headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 400)

        with db.auto_commit():
            user = User.query.filter_by(email="123456@qq.com").first()
            library = Library.query.filter_by(name="test_library").first()
            user.selecting_library = library

        response = self.client.get(url_for("func"), headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"hello world" in response.data)

    def test_can(self):
        @self.app.route("/nothing")
        @auth_required
        @select_library
        @can("nothing")
        def nothing():
            return "nothing"

        @self.app.route("/testing")
        @auth_required
        @select_library
        @can("BORROW")
        def func():
            return "hello world"

        token = self.get_token()
        with db.auto_commit():
            user = User.query.filter_by(email="123456@qq.com").first()
            library = Library.query.filter_by(name="test_library").first()
            user.selecting_library = library
        response = self.client.get(url_for("nothing"), headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 403)

        response = self.client.get(url_for("func"), headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"hello world" in response.data)


if __name__ == "__main__":
    unittest.main()
