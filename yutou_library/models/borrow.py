from sqlalchemy.sql import func

from yutou_library.extensions import db
from yutou_library.libs.enums import BorrowState


class Borrow(db.Model):
    __tablename__ = "borrow"

    id = db.Column("br_id", db.Integer, primary_key=True)
    uid = db.Column("u_id", db.Integer, db.ForeignKey("user.u_id"), nullable=False)
    lid = db.Column("l_id", db.Integer, db.ForeignKey("library.l_id"))
    bid = db.Column("b_id", db.Integer, db.ForeignKey("book.b_id"))
    borrow_date = db.Column(db.DateTime)
    deadtime = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime, nullable=True)
    create_date = db.Column(db.DateTime, server_default=func.now())
    state = db.Column("state", db.Enum(BorrowState))

    user = db.relationship("User", back_populates="borrows")
    book = db.relationship("Book")
    library = db.relationship("Library", back_populates="borrows")
