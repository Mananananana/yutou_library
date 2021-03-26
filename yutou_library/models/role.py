from yutou_library.extensions import db


class Role(db.Model):
    id = db.Column("r_id", db.Integer, primary_key=True)
    lid = db.Column("l_id", db.Integer, db.ForeignKey("library.l_id"))
    name = db.Column("r_name", db.String(16), nullable=False)
