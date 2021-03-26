from yutou_library.extensions import db


class Attribute(db.Model):
    __tablename__ = "attribute"

    lid = db.Column("l_id", db.Integer, db.ForeignKey("library.l_id"), primary_key=True)
    uid = db.Column("u_id", db.Integer, db.ForeignKey("user.u_id"), primary_key=True)

    rid = db.Column("r_id", db.Integer, db.ForeignKey("role.r_id"))
    type = db.Column("rt_id", db.Integer, db.ForeignKey("rtype.rt_id"))

    library = db.relationship("Library", back_populates="attributes", lazy="joined")
    user = db.relationship("User", back_populates="attributes", lazy="joined")
    rtype = db.relationship("RType")
