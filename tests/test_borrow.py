import unittest

from flask import url_for

from tests.base import BaseTestCase
from yutou_library.models import Borrow
from yutou_library.libs.enums import BookStatus


class BorrowTestCase(BaseTestCase):
    def test_borrow_book(self):
        response = self.client.post(url_for("api_v1.borrow_api", bid=self.normal_book.id),
                                    token=self.get_token(self.under_review))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(url_for("api_v1.borrow_api", bid=self.normal_book.id),
                                    token=self.get_token(self.user))
        self.assertEqual(response.status_code, 201)
        borrow = Borrow.query.filter_by(bid=self.normal_book.id).first()
        self.assertIsNotNone(borrow)
        self.assertEqual(borrow.uid, self.user.id)
        self.assertEqual(borrow.lid, self.normal_book.lid)
        self.assertIsNone(borrow.return_date)
        self.assertEqual(self.normal_book.status, BookStatus.B)

    def test_return_book(self):
        response = self.client.put(url_for("api_v1.borrow_api", bid=self.borrowed_book.id),
                                   token=self.get_token(self.creator))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.borrowed_book.status, BookStatus.A)
        borrow = Borrow.query.filter_by(bid=self.borrowed_book.id).first()
        self.assertIsNotNone(borrow.return_date)

    def test_get_borrow_info(self):
        response = self.client.get(url_for("api_v1.borrows_api"), token=self.get_token(self.creator))
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["size"], len(data["borrows"]))


if __name__ == "__main__":
    unittest.main()
