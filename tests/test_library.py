import unittest

from flask import url_for

from tests.base import BaseTestCase
from yutou_library.models import User, Attribution, Library
from yutou_library.extensions import db
from yutou_library.libs.enums import AttributeLevel, AttributeStatus, LibraryStatus


class LibraryTestCase(BaseTestCase):
    def test_get_libraries(self):
        token = self.get_token()
        response = self.client.get(url_for("api_v1.libraries_api"), headers=[("Authorization", "Bearer " + token)])
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["size"], len(data["libraries"]))

    def test_create_library(self):
        token = self.get_token()
        response = self.client.post(url_for("api_v1.libraries_api"), headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.libraries_api"),
                                    json={"name": "hfhquh qu23 "},
                                    headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.libraries_api"),
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
        token = self.get_token()
        response = self.client.get(url_for("api_v1.library_api", lid=self.creator.selecting_library_id),
                                   headers=[("Authorization", "Bearer " + token)])
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data["id"], int))
        self.assertEqual(data["name"], "test_library")
        self.assertEqual(data["status"], "normal")
        self.assertTrue(isinstance(data["create_date"], int))

    def test_update_library_info(self):
        token = self.get_token()
        lid = self.creator.selecting_library_id
        response = self.client.patch(url_for("api_v1.library_api", lid=lid), json={"name": "34j8erht834hturhvu$i2"},
                                     headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(url_for("api_v1.library_api", lid=lid), json={"name": "this is a test"},
                                     headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 201)
        library = Library.query.get(lid)
        self.assertIsNotNone(library)
        self.assertEqual(library.name, "this is a test")

    def test_join_library(self):
        token = self.get_token()
        lid = self.creator.selecting_library_id
        response = self.client.get(url_for("api_v1.join_library", lid=lid),
                                   headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 403)

        with db.auto_commit():
            user = User(name="testUser", gender="m", phone="13412345678", email="654321@qq.com")
            user.set_password("123456")
            db.session.add(user)
        token = self.get_token(user)
        lid = self.library.id
        response = self.client.get(url_for("api_v1.join_library", lid=lid),
                                   headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 201)
        attribute = Attribution.query.filter_by(uid=user.id, lid=lid).first()
        self.assertIsNotNone(attribute)
        self.assertEqual(attribute.level, AttributeLevel.D)
        self.assertEqual(attribute.status, AttributeStatus.A)
        self.assertEqual(attribute.type, "copper reader")

    def test_select_library(self):
        self.assertEqual(self.admin.selecting_library_id, self.library.id)
        token = self.get_token(self.admin)
        lid = self.library2.id
        response = self.client.get(url_for("api_v1.select_library", lid=lid),
                                   headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.admin.selecting_library_id, lid)

        with db.auto_commit():
            library = Library(name="test_library2", status=LibraryStatus.A)
            db.session.add(library)
        response = self.client.get(url_for("api_v1.select_library", lid=library.id),
                                   headers=[("Authorization", "Bearer " + token)])
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
