# todo: test book module
import unittest

from flask import url_for

from tests.base import BaseTestCase
from yutou_library.extensions import db
from yutou_library.libs.enums import BookStatus
from yutou_library.models import Book


class BookTestCase(BaseTestCase):
    def test_get_book_info(self):
        response = self.client.get(url_for("api_v1.book_api", bid=self.normal_book.id),
                                   token=self.get_token(self.under_review))
        self.assertEqual(response.status_code, 400)
        with db.auto_commit():
            self.under_review.selecting_library_id = self.library.id
        response = self.client.get(url_for("api_v1.book_api", bid=self.normal_book.id),
                                   token=self.get_token(self.under_review))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(url_for("api_v1.book_api", bid=self.normal_book.id), token=self.get_token())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], self.normal_book.id)
        self.assertEqual(data["lid"], self.normal_book.lid)
        self.assertEqual(data["isbn"], self.normal_book.isbn)
        self.assertEqual(data["status"], self.normal_book.status.value)
        self.assertEqual(data["title"], self.normal_book.title)
        self.assertEqual(data["author"], self.normal_book.author)

    def test_modify_book_info(self):
        response = self.client.patch(url_for("api_v1.book_api", bid=self.normal_book.id),
                                     token=self.get_token(self.user),
                                     json=dict(isbn="1234567891012",
                                               status=BookStatus.B.value,
                                               title="test123",
                                               author="321test"))
        self.assertEqual(response.status_code, 403)
        response = self.client.patch(url_for("api_v1.book_api", bid=self.normal_book.id),
                                     token=self.get_token(), json=dict(isbn="1234567891012",
                                                                       status=BookStatus.B.value,
                                                                       title="test123",
                                                                       author="321test"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.normal_book.isbn, "1234567891012")
        self.assertEqual(self.normal_book.status, BookStatus.B)
        self.assertEqual(self.normal_book.title, "test123")
        self.assertEqual(self.normal_book.author, "321test")

    def test_delete_book(self):
        response = self.client.delete(url_for("api_v1.book_api", bid=self.normal_book.id),
                                      token=self.get_token(self.user))
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(url_for("api_v1.book_api", bid=self.normal_book.id),
                                      token=self.get_token())
        self.assertEqual(response.status_code, 202)
        self.assertEqual(Book.query.count(), 3)

    def test_add_book(self):
        response = self.client.post(url_for("api_v1.books_api"),
                                    token=self.get_token(self.user))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(url_for("api_v1.books_api"),
                                    token=self.get_token(),
                                    json=dict(isbn="1234567891012",
                                              title="test123",
                                              author="321test"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.query.count(), 5)

    def test_get_books(self):
        response = self.client.get(url_for("api_v1.books_api"),
                                   token=self.get_token(self.user))
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["size"], len(data["books"]))

    def test_get_book_detail(self):
        response = self.client.get(url_for("api_v1.book_detail_api", isbn=123456798))
        self.assertEqual(response.status_code, 401)

        response = self.client.get(url_for("api_v1.book_detail_api", isbn=9787302444541))
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue("_id" in data)
        self.assertEqual(data["_id"], "9787302444541")

        response = self.client.get(url_for("api_v1.book_detail_api", isbn=9787302444543))
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue("_id" in data)
        self.assertEqual(data["_id"], "9787302444541")


if __name__ == '__main__':
    unittest.main()
