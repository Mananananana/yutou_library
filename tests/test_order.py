import unittest

from flask import url_for

from tests.base import BaseTestCase
from yutou_library.models import Borrow
from yutou_library.libs.enums import BookStatus, BorrowState


class OrderTestCase(BaseTestCase):
    def test_create_order(self):
        response = self.client.post(url_for("api_v1.order_api", bid=self.normal_book.id + 1000), token=self.get_token())
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.normal_book.status, BookStatus.A)
        response = self.client.post(url_for("api_v1.order_api", bid=self.normal_book.id), token=self.get_token())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Borrow.query.filter_by(state=BorrowState.C).count(), 1)
        order = Borrow.query.filter_by(bid=self.normal_book.id, uid=self.creator.id).first()
        self.assertIsNotNone(order)
        self.assertEqual(self.normal_book.status, BookStatus.E)

    def test_delete_order(self):
        self.assertEqual(self.normal_book.status, BookStatus.A)
        response = self.client.post(url_for("api_v1.order_api", bid=self.normal_book.id), token=self.get_token())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.normal_book.status, BookStatus.E)

        response = self.client.delete(url_for("api_v1.order_api", bid=self.normal_book.id), token=self.get_token())
        self.assertEqual(response.status_code, 202)
        self.assertEqual(Borrow.query.filter_by(state=BorrowState.C).count(), 0)
        self.assertEqual(Borrow.query.filter_by(state=BorrowState.D).count(), 1)
        self.assertEqual(self.normal_book.status, BookStatus.A)

    def test_get_orders(self):
        response = self.client.get(url_for("api_v1.orders_api"), token=self.get_token())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["size"], len(data["orders"]))


if __name__ == "__main__":
    unittest.main()
