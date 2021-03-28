from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from yutou_library.extensions import db
from yutou_library.libs.enums import Gender
from yutou_library.models import Attribute, Permission


class User(db.Model):
    __tablename__ = "user"

    id = db.Column("u_id", db.Integer,
                   db.Sequence("users_uid_seq", start=10000),
                   primary_key=True)
    name = db.Column("u_name", db.String(16), nullable=True)
    gender = db.Column("u_sex", db.Enum(Gender), nullable=True)
    phone = db.Column("u_tel", db.String(11), unique=True, index=True)
    email = db.Column("u_email", db.String(50), unique=True, index=True)
    register_date = db.Column("u_date", db.DateTime, server_default=func.now())
    _password = db.Column("u_password", db.String(128), nullable=False)
    selecting_library_id = db.Column("selecting_library", db.Integer, db.ForeignKey("library.l_id"), nullable=True)

    attributes = db.relationship("Attribute", back_populates="user", cascade="all")
    borrows = db.relationship("Borrow", back_populates="user")
    selecting_library = db.relationship("Library")

    def set_password(self, raw):
        self._password = generate_password_hash(raw)

    def validate_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    def can(self, permission_name, lid=None):
        permission = Permission.query.filter_by(name=permission_name).first()
        attribute = Attribute.query.filter_by(uid=self.id, lid=lid or self.selecting_library_id).first()
        if attribute is None:
            return False
        return permission in attribute.role.permissions
