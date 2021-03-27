from wtforms import IntegerField
from wtforms.validators import ValidationError

from yutou_library.validators.base import BaseForm, Optional
from yutou_library.models import RType, Role

# todo: test member form


class MemberForm(BaseForm):
    type = IntegerField(validators=[Optional()])
    rid = IntegerField(validators=[Optional()])

    def validate_type(self, field):
        rtype = RType.query.get(field.data)
        if rtype is None:
            raise ValidationError(f"{field.data} is not a legal type id")

    def validate_rid(self, field):
        role = Role.query.get(field.data)
        if role is None:
            raise ValidationError(f"{field.data} is not a legal role id")
