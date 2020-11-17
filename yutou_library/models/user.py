from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from yutou_library.extensions import db
from yutou_library.libs.enums import Gender

# TODO: ADD IS_ADMIN PROPERTY
# TODO: ADD FUNCTION CAN(PERMISSION_NAME)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column("u_id", db.Integer,
                   db.Sequence("users_uid_seq", start=111111111),
                   primary_key=True)
    name = db.Column("u_name", db.String(50), nullable=True)
    gender = db.Column("u_sex", db.Enum(Gender), nullable=True)
    phone = db.Column("u_tel", db.String(11), unique=True, index=True)
    email = db.Column("u_email", db.String(50), unique=True, index=True)
    register_date = db.Column("u_date", db.DateTime, server_default=func.now())
    _password = db.Column("u_password", db.String(128), nullable=False)
    selecting_library_id = db.Column("selecting_library", db.Integer, db.ForeignKey("libraries.l_id"), nullable=True)

    attributes = db.relationship("Attribution", back_populates="user", cascade="all")
    borrows = db.relationship("Borrow", back_populates="user")
    selecting_library = db.relationship("Library")

    def set_password(self, raw):
        self._password = generate_password_hash(raw)

    def validate_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
