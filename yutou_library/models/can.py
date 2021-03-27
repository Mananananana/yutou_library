from yutou_library.extensions import db


Can = db.Table(
    "can",
    db.Column("r_id", db.Integer, db.ForeignKey("role.r_id")),
    db.Column("p_id", db.Integer, db.ForeignKey("permission.p_id"))
)
