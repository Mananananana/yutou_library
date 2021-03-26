from yutou_library.extensions import db


class Can(db.Model):
    rid = db.Column("r_id", db.Integer, db.ForeignKey("role.r_id"), primary_key=True)
    pid = db.Column("p_id", db.Integer, db.ForeignKey("permission.p_id"), primary_key=True)
