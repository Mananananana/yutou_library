from sqlalchemy.sql import func

from yutou_library.extensions import db


class Borrow(db.Model):
    __tablename__ = "borrow"
    # __table_args__ = (
    #     db.ForeignKeyConstraint(
    #         ("l_id", "b_id"),
    #         ["book.l_id", "book.b_id"]
    #     ),
    # )

    id = db.Column(db.String(50), primary_key=True)
    uid = db.Column("u_id", db.Integer, db.ForeignKey("users.u_id"), nullable=False)
    lid = db.Column("l_id", db.Integer, db.ForeignKey("libraries.l_id"))
    bid = db.Column("b_id", db.Integer, db.ForeignKey("book.b_id"))
    borrow_date = db.Column(db.DateTime, server_default=func.now())
    deadtime = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="borrows")
    book = db.relationship("Book")
    library = db.relationship("Library", back_populates="borrows")
