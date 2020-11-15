from yutou_library.extensions import db


class LibraryMeta(db.Model):
    __tablename__ = "librarymeta"

    id = db.Column("meta_id", db.Integer, primary_key=True, autoincrement=True)
    lid = db.Column("l_id", db.Integer, db.ForeignKey("libraries.l_id"))
    key = db.Column("meta_key", db.String(100))
    value = db.Column("meta_value", db.String(500))

    library = db.relationship("Library", back_populates="metas")
