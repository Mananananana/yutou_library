from yutou_library.extensions import db
from yutou_library.libs.enums import BookStatus


class Book(db.Model):
    __tablename__ = "book"

    id = db.Column("b_id", db.Integer, primary_key=True, autoincrement=True)
    lid = db.Column("l_id", db.Integer, db.ForeignKey("library.l_id"), nullable=False)

    isbn = db.Column(db.String(13), nullable=False)
    status = db.Column("b_status", db.Enum(BookStatus))
    title = db.Column("b_name", db.String(64))
    author = db.Column("b_author", db.String(64))
    image_urls = db.Column("b_image_url", db.String(150))

    library = db.relationship("Library", back_populates="books")
