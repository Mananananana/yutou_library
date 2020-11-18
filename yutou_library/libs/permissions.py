PERMISSIONS = ("BORROW", "ORDER", "READ_BOOK_INFO", "UPDATE_BOOK_INFO",
               "ADD_BOOK", "DELETE_BOOK", "UPDATE_LIBRARY_INFO",
               "READ_MEMBER_INFO", "UPDATE_MEMBER_INFO", "DELETE_MEMBER")

ADMINS = ("creator", "admin")

role_permission_map = {
    "creator": PERMISSIONS,
    "admin": ("BORROW", "ORDER", "READ_BOOK_INFO", "UPDATE_BOOK_INFO",
              "ADD_BOOK", "READ_MEMBER_INFO", "UPDATE_MEMBER_INFO"),
    "user": ("BORROW", "ORDER", "READ_BOOK_INFO", "READ_MEMBER_INFO"),
    "under_review": ()
}
