from yutou_library.extensions import db


class RType(db.Model):
    __tablename__ = "rtype"

    id = db.Column("rt_id", db.String(50), primary_key=True)
    date = db.Column("rt_date", db.Integer, nullable=False)
    num = db.Column("rt_num", db.Integer, nullable=False)
    mean = db.Column("rt_mean", db.String(50))
