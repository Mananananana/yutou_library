import re

from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp

from yutou_library.validators.base import BaseForm


class LibraryForm(BaseForm):
    name = StringField(validators=[
        DataRequired(),
        Length(min=2, max=16),
        Regexp(r"\w+", flags=re.U,
               message="Not allow special character!")
    ])
