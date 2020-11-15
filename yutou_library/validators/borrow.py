from wtforms import IntegerField
from wtforms.validators import DataRequired

from yutou_library.validators.base import BaseForm


class BorrowForm(BaseForm):
    bid = IntegerField(validators=[DataRequired()])
    lid = IntegerField(validators=[DataRequired()])
