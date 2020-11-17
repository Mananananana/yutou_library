import unittest

from flask import url_for

from yutou_library import create_app
from yutou_library.extensions import db
from yutou_library.models import User, Library, Attribution, RType
from yutou_library.libs.enums import LibraryStatus, AttributeLevel, AttributeStatus


class BaseTestCase(unittest.TestCase):
    def get_token(self):
        response = self.client.post(url_for("api_v1.login"), json={"method": "phone",
                                                                   "phone": '13912345678',
                                                                   "password": "123456"})
        data = response.get_json()
        return data["token"]

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

        db.create_all()

        user = User(email="123456@qq.com", phone="13912345678", gender="m", name="laichaoqun")
        user.set_password("123456")
        test_library = Library(name="test_library", status=LibraryStatus.A)
        rtype = RType(id="golden reader", date=100, num=10)
        rtype2 = RType(id="sliver reader", date=50, num=5)
        rtype3 = RType(id="copper reader", date=25, num=3)

        db.session.add(user)
        db.session.add(test_library)
        db.session.add(rtype)
        db.session.add(rtype2)
        db.session.add(rtype3)

        db.session.flush()

        attribute = Attribution(uid=user.id, lid=test_library.id,
                                level=AttributeLevel.A, status=AttributeStatus.A,
                                type=rtype.id)
        db.session.add(attribute)
        db.session.commit()

    def tearDown(self) -> None:
        db.drop_all()
        self.context.pop()

    def test_base(self):
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(Library.query.count(), 1)
        self.assertEqual(RType.query.count(), 3)
        self.assertEqual(Attribution.query.count(), 1)


if __name__ == "__main__":
    unittest.main()
