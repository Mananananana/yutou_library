from sqlalchemy.sql import func

from yutou_library.extensions import db
from yutou_library.libs.enums import LibraryStatus


class Library(db.Model):
    __tablename__ = "libraries"

    id = db.Column("l_id", db.Integer,
                   db.Sequence("library_lid_seq", start=100000000, increment=1),
                   primary_key=True)
    name = db.Column("l_name", db.String(50), nullable=False)
    status = db.Column("l_status", db.Enum(LibraryStatus), nullable=False)
    create_date = db.Column("l_date", db.DateTime, server_default=func.now())

    attributes = db.relationship("Attribution", back_populates="library", cascade="all")
    metas = db.relationship("LibraryMeta", back_populates="library", cascade="all")
    books = db.relationship("Book", back_populates="library", cascade="all")
    borrows = db.relationship("Borrow", back_populates="library", cascade="all")
    orders = db.relationship("Order", back_populates="library", cascade="all")
