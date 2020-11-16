from flask import jsonify


from yutou_library.apis.v1 import api_v1
from yutou_library.libs.enums import LoginMethod
from yutou_library.validators.account import EmailLoginForm, PhoneLoginForm, RegisterForm, MethodForm
from yutou_library.models import User
from yutou_library.extensions import db
from yutou_library.libs.error_code import EmailAlreadyExist, PhoneAlreadyExist, Success, AuthFailed
from yutou_library.apis.v1.auth import generate_token


methods = {
    LoginMethod.by_email: EmailLoginForm,
    LoginMethod.by_phone: PhoneLoginForm,
}


@api_v1.route("/account/register", methods=["POST"])
def register():
    """
    用户注册
    :param email:用户邮箱
    :param phone:用户手机号
    :param password:用户明文密码
    :return:
    """
    form = RegisterForm().validate_for_api()
    email = form.email.data
    phone = form.phone.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()
    if user is not None:
        return EmailAlreadyExist()
    user = User.query.filter_by(phone=phone).first()
    if user is not None:
        return PhoneAlreadyExist()

    with db.auto_commit():
        user = User(email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
    return Success()


@api_v1.route("/account/login", methods=["POST"])
def login():
    method_form = MethodForm().validate_for_api()
    method = method_form.method.data
    form = methods[method]()
    if method == LoginMethod.by_phone:
        phone = form.phone.data
        user = User.query.filter_by(phone=phone).first()
    elif method == LoginMethod.by_email:
        email = form.email.data
        user = User.query.filter_by(email=email).first()
    else:
        user = None
    password = form.password.data

    if user is not None and user.validate_password(password):
        token, expire_in = generate_token(user)
        return jsonify(dict(token=token, expire_in=expire_in)), 201
    return AuthFailed()


@api_v1.route("/account", methods=["PATCH"])
def modify_info():
    pass


@api_v1.route("/account", methods=["GET"])
def get_info():
    pass


@api_v1.route("/account/libraries", methods=["GET"])
def get_libraries():
    pass
