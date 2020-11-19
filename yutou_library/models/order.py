from datetime import datetime, timedelta

from yutou_library.extensions import db


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column("u_id", db.Integer, db.ForeignKey("users.u_id"), nullable=False)
    lid = db.Column("l_id", db.Integer, db.ForeignKey("libraries.l_id"), nullable=False)
    bid = db.Column("b_id", db.Integer, db.ForeignKey("book.b_id"), nullable=False)
    effective_date = db.Column(db.DateTime, default=datetime.utcnow())
    invalid_date = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(3))

    user = db.relationship("User", back_populates="orders")
    library = db.relationship("Library", back_populates="orders")
    book = db.relationship("Book")
