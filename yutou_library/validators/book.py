from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp

from yutou_library.validators.base import BaseForm


class BookForm(BaseForm):
    lid = IntegerField(validators=[DataRequired()])
    title = StringField(validators=[Length(min=1, max=150)])
    author = StringField(validators=[Length(min=1, max=150)])
    isbn = StringField(validators=[DataRequired(), Regexp(r"\d{13}")])


class BookUpdateForm(BookForm):
    bid = IntegerField(validators=[DataRequired()])
