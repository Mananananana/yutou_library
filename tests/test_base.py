import unittest

from tests.base import BaseTestCase
from yutou_library.models import User, Library, RType, Attribute, Book, Borrow, Permission, Role, Can
from yutou_library.libs.permissions import PERMISSIONS, ROLES, role_permission_map


class BaseTestTestCase(BaseTestCase):
    def test_base(self):
        self.assertEqual(User.query.count(), 4)
        self.assertEqual(Library.query.count(), 2)
        self.assertEqual(RType.query.count(), 3)
        self.assertEqual(Attribute.query.count(), 5)
        self.assertEqual(Book.query.count(), 4)
        self.assertEqual(Borrow.query.count(), 1)
        self.assertEqual(Permission.query.count(), len(PERMISSIONS))
        self.assertEqual(Role.query.count(), len(ROLES))


if __name__ == "__main__":
    unittest.main()
