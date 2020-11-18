from functools import wraps

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, request, g

from yutou_library.models import User, Attribution
from yutou_library.libs.error_code import TokenTypeError, TokenMissing, InvalidToken, \
    NotSelectedLibrary, PermissionDenied, NoLibraryId


PERMISSIONS = ("BORROW", "ORDER", "READ_BOOK_INFO", "UPDATE_BOOK_INFO",
               "ADD_BOOK", "DELETE_BOOK", "UPDATE_LIBRARY_INFO",
               "READ_MEMBER_INFO", "UPDATE_MEMBER_INFO", "DELETE_MEMBER")

role_permission_map = {
    "creator": PERMISSIONS,
    "admin": ("BORROW", "ORDER", "READ_BOOK_INFO", "UPDATE_BOOK_INFO",
              "ADD_BOOK", "READ_MEMBER_INFO", "UPDATE_MEMBER_INFO"),
    "user": ("BORROW", "ORDER", "READ_BOOK_INFO", "READ_MEMBER_INFO"),
    "under_review": ()
}


def generate_token(user, expires_in=3600, **kwargs):
    """
    为用户生成token
    :param user: 认证用户， User模型实例
    :param expires_in: token过期时间
    :param kwargs: 添加到token中的附加参数
    :return:
    """
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expires_in)
    token = s.dumps(dict(id=user.id, **kwargs)).decode("ascii")
    return token, expires_in


def validate_token(token):
    """
    验证JWT token
    :param token: 要验证的token令牌
    :return: 验证结果
    """
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return False
    user = User.query.get(data["id"])
    if user is None:
        return False
    g.current_user = user
    return True


def get_token():
    """
    从请求首部中获取token，如果获取失败则返回None
    """
    try:
        token_type, token = request.headers["Authorization"].split(None, 1)
    except (KeyError, ValueError):
        token_type = token = None
    return token_type, token


def auth_required(func):
    """
    认证保护装饰器，没有token或token错误时禁止用户访问
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        if request.method != "OPTIONS":
            token_type, token = get_token()
            if token_type is None or token_type.lower() != "bearer":
                return TokenTypeError()
            if token is None:
                return TokenMissing()
            if not validate_token(token):
                return InvalidToken()
        return func(*args, **kwargs)
    return decorator


def select_library(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        user = g.current_user
        if user.selecting_library_id is None:
            return NotSelectedLibrary()
        return func(*args, **kwargs)
    return decorator


def can(permission_name, library_id=None):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            user = g.current_user
            lid = library_id or user.selecting_library_id
            if lid is None:
                return NoLibraryId()
            attribute = Attribution.query.filter_by(uid=user.id, lid=lid).first()
            if attribute is None:
                return PermissionDenied()
            permissions = role_permission_map[attribute.level.value]
            if permission_name not in permissions:
                return PermissionDenied()
            return func(*args, **kwargs)
        return decorator
    return wrapper
