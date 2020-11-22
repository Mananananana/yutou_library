from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

from yutou_library.validators.base import BaseForm, Optional
from yutou_library.libs.enums import BookStatus


class BookForm(BaseForm):
    title = StringField(validators=[Length(min=1, max=150)])
    author = StringField(validators=[Length(min=1, max=150)])
    isbn = StringField(validators=[DataRequired(), Regexp(r"\d{13}")])


class BookUpdateForm(BookForm):
    status = StringField(validators=[Optional()])

    def validate_status(self, field):
        try:
            self.status.data = BookStatus(field.data)
        except ValueError:
            raise ValidationError(f"{field.data} is not a illegal value")
