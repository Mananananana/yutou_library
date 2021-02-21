from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError, URL

from yutou_library.validators.base import BaseForm, Optional
from yutou_library.libs.enums import BookStatus


class BookForm(BaseForm):
    title = StringField(validators=[Optional(), Length(min=1, max=150)])
    author = StringField(validators=[Optional(), Length(min=1, max=150)])
    isbn = StringField(validators=[Optional(), Regexp(r"\d{13}")])
    image_urls = StringField(validators=[Optional(), URL()])


class BookUpdateForm(BookForm):
    status = StringField(validators=[Optional()])

    def validate_status(self, field):
        try:
            self.status.data = BookStatus(field.data)
        except ValueError:
            raise ValidationError(f"{field.data} is not a illegal value")
