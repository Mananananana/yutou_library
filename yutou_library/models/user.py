from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from yutou_library.extensions import db
from yutou_library.libs.enums import Gender
from yutou_library.models import Attribution, Library, Borrow, Order
from yutou_library.libs.permissions import role_permission_map, ADMINS


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
    orders = db.relationship("Order", back_populates="user")
    selecting_library = db.relationship("Library")

    def set_password(self, raw):
        self._password = generate_password_hash(raw)

    def validate_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    def is_admin(self, lid):
        attribute = Attribution.query.filter_by(uid=self.id, lid=lid or self.selecting_library_id).first()
        if attribute is None:
            return False
        if attribute.level.value not in ADMINS:
            return False
        return True

    def can(self, permission_name, lid=None):
        attribute = Attribution.query.filter_by(uid=self.id, lid=lid or self.selecting_library_id).first()
        if attribute is None:
            return False
        permissions = role_permission_map[attribute.level.value]
        if permission_name not in permissions:
            return False
        return True

    def can_borrow_or_order_in(self, lid, borrow=True):
        library = Library.query.get(lid)
        if not library:
            return False
        attribute = Attribution.query.filter_by(uid=self.id, lid=lid).first()
        if not attribute:
            return False
        permissions = role_permission_map[attribute.level.value]
        if borrow:
            if "BORROW" not in permissions:
                return False
        else:
            if "ORDER" not in permissions:
                return False
        borrow_count = Borrow.query.filter_by(uid=self.id, lid=lid).count()
        order_count = Order.query.filter_by(uid=self.id, lid=lid).count()
        rtype = attribute.rtype
        if borrow_count + order_count >= rtype.num:
            return False
        return rtype.date
