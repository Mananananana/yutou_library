from yutou_library.extensions import db


class RType(db.Model):
    __tablename__ = "rtype"

    id = db.Column("rt_id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("rt_name", db.String(16))
    date = db.Column("rt_date", db.Integer, nullable=False)
    num = db.Column("rt_num", db.Integer, nullable=False)
