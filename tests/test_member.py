import unittest

from flask import url_for

from tests.base import BaseTestCase
from yutou_library.models import Attribute


class MemberTestCase(BaseTestCase):
    def test_update_member_info(self):
        response = self.client.put(url_for("api_v1.member_api", uid=self.creator.id),
                                   json={}, token=self.get_token())
        self.assertEqual(response.status_code, 201)
        attribute = Attribute.query.filter_by(lid=self.library.id, uid=self.creator.id).first()
        self.assertIsNotNone(attribute)
        self.assertEqual(attribute.type, self.golden.id)

        response = self.client.put(url_for("api_v1.member_api", uid=self.creator.id), token=self.get_token(),
                                   json={
                                       "type": self.sliver.id
                                   })
        self.assertEqual(response.status_code, 201)
        attribute = Attribute.query.filter_by(lid=self.library.id, uid=self.creator.id).first()
        self.assertEqual(attribute.type, self.sliver.id)

    def test_delete_member(self):
        attribute = Attribute.query.filter_by(lid=self.library.id, uid=self.user.id).first()
        self.assertIsNotNone(attribute)
        response = self.client.delete(url_for("api_v1.member_api", uid=self.user.id), token=self.get_token())
        self.assertEqual(response.status_code, 202)
        attribute = Attribute.query.filter_by(lid=self.library.id, uid=self.user.id).first()
        self.assertIsNone(attribute)

    def test_get_members_info(self):
        response = self.client.get(url_for("api_v1.members_api"), token=self.get_token())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["size"], len(data["members"]))


if __name__ == "__main__":
    unittest.main()
