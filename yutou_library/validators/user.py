from wtforms import StringField, ValidationError
from wtforms.validators import Length, Regexp, StopValidation

from yutou_library.validators.base import BaseForm, Optional
from yutou_library.libs.enums import Gender


class UserForm(BaseForm):
    name = StringField(validators=[Optional(), Length(min=3, max=16), Regexp(r"^[\w\d_-]{3,16}$")])
    gender = StringField(validators=[Optional()])

    def validate_gender(self, field):
        try:
            self.gender.data = Gender(field.data)
        except ValueError:
            raise ValidationError(f"{field.data} is not an illegal gender")
