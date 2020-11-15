from yutou_library.extensions import db
from yutou_library.libs.enums import AttributeLevel, AttributeStatus


class Attribution(db.Model):
    __tablename__ = "attribution"

    libraries = db.relationship("Library")
    users = db.relationship("User")
    rtype = db.relationship("RType")

    lid = db.Column("l_id", db.Integer, db.ForeignKey("libraries.l_id"), primary_key=True)
    uid = db.Column("u_id", db.Integer, db.ForeignKey("users.u_id"), primary_key=True)

    level = db.Column("a_level", db.Enum(AttributeLevel))
    status = db.Column("a_status", db.Enum(AttributeStatus))
    type = db.Column("a_type", db.String(50), db.ForeignKey("rtype.rt_id"))
