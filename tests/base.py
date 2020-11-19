import unittest
from datetime import datetime, timedelta

from flask.testing import FlaskClient as _FlaskClient

from yutou_library import create_app
from yutou_library.extensions import db
from yutou_library.models import User, Library, Attribution, RType, Book, Borrow
from yutou_library.libs.enums import LibraryStatus, AttributeLevel, AttributeStatus, BookStatus
from yutou_library.apis.v1.auth import generate_token


class FlaskClient(_FlaskClient):
    def open(self, *args, **kwargs):
        token = kwargs.pop("token", None)
        if token:
            authorization = [("Authorization", "Bearer " + token)]
            headers = kwargs.get("headers", [])
            headers.extend(authorization)
            kwargs["headers"] = headers
        return super(_FlaskClient, self).open(*args, **kwargs)


class BaseTestCase(unittest.TestCase):
    def get_token(self, user=None):
        if user is None:
            user = self.creator
        token, expires_in = generate_token(user)
        return token

    def generate_test_users(self):
        with db.auto_commit():
            self.creator = User(email="123456@qq.com", phone="13912345678", gender="m", name="creator")
            self.admin = User(email="234567@qq.com", phone="13812345678", gender="m", name="admin")
            self.user = User(email="345678@qq.com", phone="13712345678", gender="m", name="user")
            self.under_review = User(email="456789@qq.com", phone="13612345678", gender="m", name="under_review")

            self.creator.set_password("123456")
            self.admin.set_password("123456")
            self.user.set_password("123456")
            self.under_review.set_password("123456")

            db.session.add(self.creator)
            db.session.add(self.admin)
            db.session.add(self.user)
            db.session.add(self.under_review)

    def generate_test_libraries(self):
        with db.auto_commit():
            self.library = Library(name="test_library", status=LibraryStatus.A)
            self.library2 = Library(name="test_library2", status=LibraryStatus.A)
            db.session.add(self.library)
            db.session.add(self.library2)

    def generate_test_rtype(self):
        with db.auto_commit():
            golden = RType(id="golden reader", date=100, num=10)
            sliver = RType(id="sliver reader", date=50, num=5)
            copper = RType(id="copper reader", date=25, num=3)

            db.session.add(golden)
            db.session.add(sliver)
            db.session.add(copper)

    def generate_test_attributions(self):
        with db.auto_commit():
            creator_attribute = Attribution(uid=self.creator.id, lid=self.library.id,
                                            level=AttributeLevel.A, status=AttributeStatus.A,
                                            type="golden reader")
            admin_attribute = Attribution(uid=self.admin.id, lid=self.library.id,
                                          level=AttributeLevel.B, status=AttributeStatus.A,
                                          type="sliver reader")
            user_attribute = Attribution(uid=self.user.id, lid=self.library.id,
                                         level=AttributeLevel.C, status=AttributeStatus.A,
                                         type="copper reader")
            under_review_attribute = Attribution(uid=self.under_review.id, lid=self.library.id,
                                                 level=AttributeLevel.D, status=AttributeStatus.A,
                                                 type="copper reader")

            admin_attribute2 = Attribution(uid=self.admin.id, lid=self.library2.id,
                                           level=AttributeLevel.A, status=AttributeStatus.A,
                                           type="golden reader")

            db.session.add(creator_attribute)
            db.session.add(admin_attribute)
            db.session.add(user_attribute)
            db.session.add(under_review_attribute)
            db.session.add(admin_attribute2)

    def generate_test_books(self):
        with db.auto_commit():
            self.normal_book = Book(lid=self.library.id, status=BookStatus.A,
                                    title="test1", author="nobody", isbn="1234567891011")
            self.borrowed_book = Book(lid=self.library.id, status=BookStatus.B,
                                      title="test2", author="nobody", isbn="1234567891011")
            self.destroyed_book = Book(lid=self.library.id, status=BookStatus.C,
                                       title="test3", author="nobody", isbn="1234567891011")
            self.lost_book = Book(lid=self.library.id, status=BookStatus.D,
                                  title="test4", author="nobody", isbn="1234567891011")

            db.session.add(self.normal_book)
            db.session.add(self.borrowed_book)
            db.session.add(self.destroyed_book)
            db.session.add(self.lost_book)

    def generate_test_borrows(self):
        with db.auto_commit():
            borrow_date = datetime.utcnow()
            borrow = Borrow(id="1", uid=self.creator.id, lid=self.library.id,
                            bid=self.borrowed_book.id, borrow_date=borrow_date,
                            deadtime=borrow_date+timedelta(3))
            db.session.add(borrow)

    def generate_test_sample(self):
        self.generate_test_users()
        self.generate_test_libraries()
        self.generate_test_rtype()
        self.generate_test_attributions()
        self.generate_test_books()
        self.generate_test_borrows()

        with db.auto_commit():
            self.creator.selecting_library_id = self.library.id
            self.admin.selecting_library_id = self.library.id
            self.user.selecting_library_id = self.library.id

    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app.test_client_class = FlaskClient

        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

        db.create_all()

        self.generate_test_sample()

    def tearDown(self) -> None:
        db.drop_all()
        self.context.pop()


if __name__ == "__main__":
    unittest.main()
