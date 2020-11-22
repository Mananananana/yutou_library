from datetime import datetime, timedelta

from flask.views import MethodView
from flask import g, jsonify

from yutou_library.apis.v1 import api_v1
from yutou_library.apis.v1.auth import auth_required
from yutou_library.models import Book, Borrow, Attribution
from yutou_library.libs.error_code import PermissionDenied, CanNotBorrow, Success
from yutou_library.libs.enums import BookStatus
from yutou_library.extensions import db
from yutou_library.apis.v1.schemas import borrows_schema


class BorrowAPI(MethodView):
    decorators = [auth_required]

    def post(self, bid):
        book = Book.query.get_or_404(bid)
        lid = book.lid
        user = g.current_user
        if not user.can("BORROW", lid):
            return PermissionDenied()
        borrow_date = user.can_borrow_or_order_in(lid)
        if book.status != BookStatus.A or \
                borrow_date is False:
            return CanNotBorrow()

        with db.auto_commit():
            now = datetime.utcnow()
            book.status = BookStatus.B
            borrow = Borrow(id=str(int(now.timestamp())), uid=user.id,
                            lid=lid, bid=bid, borrow_date=now, deadtime=now + timedelta(borrow_date))
            db.session.add(borrow)
        return Success()

    def patch(self, bid):
        book = Book.query.get_or_404(bid)
        lid = book.lid
        user = g.current_user
        if not user.can("RETURN_BOOK", lid):
            return PermissionDenied()
        borrow = Borrow.query.filter_by(bid=bid, return_date=None).first_or_404()
        with db.auto_commit():
            borrow.return_date = datetime.utcnow()
            book.status = BookStatus.A
        return Success()


class BorrowsAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        user = g.current_user
        borrows = Borrow.query.filter_by(uid=user.id).all()
        return jsonify(borrows_schema(borrows)), 200


api_v1.add_url_rule("/borrow/<int:bid>", view_func=BorrowAPI.as_view("borrow_api"), methods=["POST", "PATCH"])
api_v1.add_url_rule("/borrow", view_func=BorrowsAPI.as_view("borrows_api"), methods=["GET"])
