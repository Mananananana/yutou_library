from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import Length, DataRequired, Email, Regexp, ValidationError

from yutou_library.validators.base import BaseForm
from yutou_library.libs.enums import LoginMethod


class MethodForm(BaseForm):
    method = IntegerField(validators=[DataRequired()])

    def validate_method(self, field):
        try:
            self.method.data = LoginMethod(field.data)
        except ValueError:
            raise ValidationError("method field illegal")


class PasswordForm(BaseForm):
    password = PasswordField(validators=[
        DataRequired(message="Not allowed empty password!"),
        Length(6, 32)
    ])


class EmailLoginForm(PasswordForm):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message="This email is illegal")])


class PhoneLoginForm(PasswordForm):
    phone = StringField(validators=[
        Regexp(r"^1[3-9]\d{9}$", message="This phone number is illegal")
    ])


class RegisterForm(PasswordForm):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message="This email is illegal")])
    phone = StringField(validators=[
        Regexp(r"^1[3-9]\d{9}$", message="This phone number is illegal")
    ])
