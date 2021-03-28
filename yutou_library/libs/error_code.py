from yutou_library.libs.error import APIException


class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 1


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake'
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'this resource are not found'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = "authorization failed"


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = "forbidden, not in scope"


class EmailAlreadyExist(APIException):
    code = 400
    msg = 'This email address has been registered'
    error_code = 1007


class PhoneAlreadyExist(APIException):
    code = 400
    msg = 'This phone number has been registered'
    error_code = 1008


class TokenTypeError(APIException):
    code = 400
    msg = "Token must be Bearer"
    error_code = 1009

    def get_headers(self, environ=None):
        """Get a list og headers."""
        return [("Content-Type", "application/json; charset=utf-8"), ("WWW-Authenticate", "Bearer")]


class TokenMissing(APIException):
    code = 401
    msg = "Authorization Failed"
    error_code = 1010

    def get_headers(self, environ=None):
        """Get a list og headers."""
        return [("Content-Type", "application/json; charset=utf-8"), ("WWW-Authenticate", "Bearer")]


class InvalidToken(APIException):
    code = 401
    msg = "Either the token was expired or invalid."
    error_code = 1011

    def get_headers(self, environ=None):
        """Get a list og headers."""
        return [("Content-Type", "application/json; charset=utf-8"), ("WWW-Authenticate", "Bearer")]


class NoLibrarySelected(APIException):
    code = 400
    msg = "you did not select any library"
    error_code = 1012


class PermissionDenied(APIException):
    code = 403
    msg = "you have no permission to do this operation"
    error_code = 1013


class NoLibraryId(APIException):
    code = 403
    msg = "You have not selected library"
    error_code = 998


class AlreadyJoin(APIException):
    code = 403
    msg = "You are already join this library"
    error_code = 1014


class BookNotFound(APIException):
    code = 404
    msg = "This book is not in this library"
    error_code = 1015


class IllegalISBN(APIException):
    code = 401
    msg = "This isbn is illegal, please check your input"
    error_code = 1016


class CanNotBorrow(Forbidden):
    error_code = 2001
    msg = "you can not borrow this book"


class CanNotOrder(Forbidden):
    error_code = 2002
    msg = "you can not order this book"


class CanNotDelete(Forbidden):
    error_code = 2003
    msg = "you can not delete this resource"
