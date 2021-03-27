from yutou_library.extensions import db

from yutou_library.models.can import Can


class Permission(db.Model):
    id = db.Column("p_id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("p_name", db.String(32), nullable=False)

    roles = db.relationship("Role", secondary=Can, back_populates="permissions")
