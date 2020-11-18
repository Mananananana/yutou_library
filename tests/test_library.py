# todo: test library module
import unittest

from flask import url_for

from tests.base import BaseTestCase
from yutou_library.models import User, Attribution, Library


class LibraryTestCase(BaseTestCase):
    def test_create_library(self):
        token = self.get_token()
        response = self.client.post(url_for("api_v1.create_library"), headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.create_library"),
                                    json={"name": "hfhquh qu23 "},
                                    headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.create_library"),
                                    json={"name": "test create library"},
                                    headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 201)

        user = User.query.filter_by(phone="13912345678").first()
        library = Library.query.filter_by(name="test create library").first()

        self.assertIsNotNone(user)
        self.assertIsNotNone(library)
        attribute = Attribution.query.filter_by(uid=user.id, lid=library.id).first()
        self.assertIsNotNone(attribute)

    def test_get_library_info(self):
        pass

    def test_update_library_info(self):
        pass


if __name__ == "__main__":
    unittest.main()
