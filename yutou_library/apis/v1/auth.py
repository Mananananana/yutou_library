from functools import wraps

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, request

from yutou_library.models import User
from yutou_library.libs.error_code import TokenTypeError, TokenMissing, InvalidToken


def generate_token(user, expires_in=3600, **kwargs):
    """

    :param user:
    :param expires_in:
    :param kwargs:
    :return:
    """
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expires_in)
    token = s.dumps(dict(id=user.id, **kwargs)).decode("ascii")
    return token, expires_in


def validate_token(token):
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
    try:
        token_type, token = request.header["Authorization"].split(None, 1)
    except (KeyError, ValueError):
        token_type = token = None
    return token_type, token


def auth_required(func):
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
