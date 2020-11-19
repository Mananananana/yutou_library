import unittest

from tests.base import BaseTestCase
from yutou_library.models import User, Library, RType, Attribution, Book, Borrow


class BaseTestTestCase(BaseTestCase):
    def test_base(self):
        self.assertEqual(User.query.count(), 4)
        self.assertEqual(Library.query.count(), 2)
        self.assertEqual(RType.query.count(), 3)
        self.assertEqual(Attribution.query.count(), 5)
        self.assertEqual(Book.query.count(), 4)
        self.assertEqual(Borrow.query.count(), 1)


if __name__ == "__main__":
    unittest.main()
