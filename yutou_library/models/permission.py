from yutou_library.extensions import db


class Permission(db.Model):
    id = db.Column("p_id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("p_name", db.String(16), nullable=False)
