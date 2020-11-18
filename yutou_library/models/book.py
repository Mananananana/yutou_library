from yutou_library.extensions import db
from yutou_library.libs.enums import BookStatus


class Book(db.Model):
    __tablename__ = "book"

    id = db.Column("b_id", db.Integer,
                   db.Sequence("book_bid_seq", start=100000000),
                   primary_key=True)
    lid = db.Column("l_id", db.Integer, db.ForeignKey("libraries.l_id"), nullable=False)

    isbn = db.Column(db.String(13), nullable=False)
    status = db.Column("b_status", db.Enum(BookStatus))
    title = db.Column("b_name", db.String(150))
    author = db.Column("b_author", db.String(150))

    library = db.relationship("Library", back_populates="books")
