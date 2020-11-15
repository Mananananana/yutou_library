from flask import Blueprint, request


from yutou_library.libs.enums import LoginMethod
from yutou_library.validators.account import EmailLoginForm, PhoneLoginForm, RegisterForm


account_bp = Blueprint("account", __name__)


@account_bp.route("/register", methods=["POST"])
def register():
    form = RegisterForm().validate_for_api()


@account_bp.route("/login", methods=["POST"])
def login():
    methods = {
        LoginMethod.by_email: EmailLoginForm,
        LoginMethod.by_phone: PhoneLoginForm,
    }


@account_bp.route("/logout", methods=["GET"])
def logout():
    pass


@account_bp.route("/", methods=["PATCH"])
def modify_info():
    pass


@account_bp.route("/", methods=["GET"])
def get_info():
    pass


@account_bp.route("/libraries", methods=["GET"])
def get_libraries():
    pass
