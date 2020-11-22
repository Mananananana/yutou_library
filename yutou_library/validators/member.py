from wtforms import StringField
from wtforms.validators import ValidationError

from yutou_library.validators.base import BaseForm, Optional
from yutou_library.libs.enums import AttributeLevel, AttributeStatus
from yutou_library.models import RType


class MemberForm(BaseForm):
    level = StringField(validators=[Optional()])
    status = StringField(validators=[Optional()])
    type = StringField(validators=[Optional()])

    def validate_level(self, field):
        try:
            self.level.data = AttributeLevel(field.data)
        except ValueError:
            raise ValidationError(f"{field.data} is not a illegal level name")

    def validate_status(self, field):
        try:
            self.status.data = AttributeStatus(field.data)
        except ValueError:
            raise ValidationError(f"{field.data} is not a illegal status name")

    def validate_type(self, field):
        rtype = RType.query.get(field.data)
        if rtype is None:
            raise ValidationError(f"{field.data} is not a illegal type name")
