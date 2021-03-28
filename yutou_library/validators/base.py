from flask import request
from wtforms import Form
from wtforms.validators import StopValidation

from yutou_library.libs.error_code import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self


class Optional(object):
    field_flags = ('optional', )

    def __init__(self, strip_whitespace=True):
        if strip_whitespace:
            self.string_check = lambda s: s.strip() if isinstance(s, str) else s
        else:
            self.string_check = lambda s: s

    def __call__(self, form, field):
        if field.data is None or not self.string_check(field.data):
            field.errors[:] = []
            raise StopValidation()
