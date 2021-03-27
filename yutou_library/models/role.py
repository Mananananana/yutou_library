from yutou_library.extensions import db

from yutou_library.models.can import Can


class Role(db.Model):
    id = db.Column("r_id", db.Integer, primary_key=True)
    name = db.Column("r_name", db.String(32), nullable=False)

    permissions = db.relationship("Permission", secondary=Can, back_populates="roles")
