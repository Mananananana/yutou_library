from enum import Enum


class LoginMethod(Enum):
    by_email = 101
    by_phone = 102
    by_wx = 103
    by_id = 104


class Gender(Enum):
    f = "female"
    m = "male"


class LibraryStatus(Enum):
    A = "normal"
    B = "closed"


class AttributeLevel(Enum):
    A = "creator"
    B = "admin"
    C = "user"
    D = "under_review"


class AttributeStatus(Enum):
    A = "normal"
    B = "ban"
    C = "cancel"


class BookStatus(Enum):
    A = "normal"
    B = "borrowed"
    C = "destroyed"
    D = "lost"
