from flask.views import MethodView
from flask import jsonify

from yutou_library.apis.v1 import api_v1
from yutou_library.apis.v1.auth import auth_required
from yutou_library.models import Book
from yutou_library.apis.v1.schemas import book_schema


# TODO: FINISH BOOK API

class BookAPI(MethodView):
    decorators = [auth_required]

    def get(self, bid):
        book = Book.query.get_or_404(bid)
        return jsonify(book_schema(book))

    def patch(self, bid):
        pass

    def delete(self, bid):
        pass


class BooksAPI(MethodView):
    def get(self):
        pass

    def post(self):
        pass


class BookDetailAPI(MethodView):
    def get(self, isbn):
        # TODO： WRITE BOOK SPIDER
        pass


api_v1.add_url_rule("/book/<int:bid>", view_func=BookAPI.as_view("book_api"), methods=["GET", "PATCH", "DELETE"])
api_v1.add_url_rule("/book", view_func=BooksAPI.as_view("books_api"), methods=["GET", "POST"])
api_v1.add_url_rule("/book/<int:isbn>/detail", view_func=BookDetailAPI.as_view("book_detail_api", methods=["GET"]))
