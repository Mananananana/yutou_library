import os
from time import time

from flask.views import MethodView
from flask import jsonify, g
from pymongo import MongoClient

from yutou_library.apis.v1 import api_v1
from yutou_library.apis.v1.auth import auth_required, select_library, can
from yutou_library.models import Book
from yutou_library.apis.v1.schemas import book_schema, books_schema
from yutou_library.libs.error_code import BookNotFound, Success, DeleteSuccess, IllegalISBN
from yutou_library.validators.book import BookForm, BookUpdateForm
from yutou_library.libs.enums import BookStatus
from yutou_library.extensions import db
from yutou_library.spider import BookSpider
from yutou_library.libs.helper import get_legal_isbn


# TODO: FINISH BOOK API

class BookAPI(MethodView):
    decorators = [select_library, auth_required]

    def get_book(self, bid):
        user = g.current_user
        lid = user.selecting_library_id
        book = Book.query.filter_by(id=bid, lid=lid).first()
        if book is None:
            return BookNotFound()
        return book

    @can("READ_BOOK_INFO")
    def get(self, bid):
        book = self.get_book(bid)
        return jsonify(book_schema(book)), 200

    @can("UPDATE_BOOK_INFO")
    def patch(self, bid):
        book = self.get_book(bid)
        form = BookUpdateForm().validate_for_api()
        with db.auto_commit():
            book.isbn = form.isbn.data
            book.status = form.status.data
            book.title = form.title.data
            book.author = form.author.data
        return Success()

    @can("DELETE_BOOK")
    def delete(self, bid):
        book = self.get_book(bid)
        with db.auto_commit():
            db.session.delete(book)
        return DeleteSuccess()


class BooksAPI(MethodView):
    decorators = [select_library, auth_required]

    @can("READ_BOOK_INFO")
    def get(self):
        user = g.current_user
        lid = user.selecting_library_id
        books = Book.query.filter_by(lid=lid).all()
        return jsonify(books_schema(books)), 200

    @can("ADD_BOOK")
    def post(self):
        form = BookForm().validate_for_api()
        isbn = form.isbn.data
        title = form.title.data
        author = form.author.data
        lid = g.current_user.selecting_library_id
        with db.auto_commit():
            book = Book(lid=lid, isbn=isbn, status=BookStatus.A, title=title, author=author)
            db.session.add(book)
        return Success()


class BookDetailAPI(MethodView):
    def __init__(self):
        super().__init__()

        uri = os.getenv("MONGO_URI", "mongodb://test:test@localhost:27017")
        database = os.getenv("MONGO_DATABASE", "test")
        collection = os.getenv("MONGO_COLLECTION", "book")

        self.client = MongoClient(uri)
        self.douban = self.client[database]
        self.book = self.douban[collection]
        self.spider = BookSpider()

    def _need_to_update(self, doc):
        if "_tm" in doc:
            current_time = time()
            update_time = doc["_tm"]
            return (current_time - update_time) > 10 * 24 * 60 * 60 * 1000
        return True

    def get(self, isbn):
        # TODO： WRITE BOOK SPIDER
        isbn = get_legal_isbn(str(isbn))
        if not isbn:
            return IllegalISBN()
        doc = self.book.find_one({"_id": isbn})
        if doc is None:
            doc = self.spider.get_book_info(isbn)
            if doc is not None and len(doc) > 0:
                self.book.insert_one(doc)
            else:
                return BookNotFound()
        else:
            if self._need_to_update(doc):
                doc = self.spider.get_book_info(isbn)
                self.book.update_one({"_id": isbn}, doc)
        return doc


api_v1.add_url_rule("/book/<int:bid>", view_func=BookAPI.as_view("book_api"), methods=["GET", "PATCH", "DELETE"])
api_v1.add_url_rule("/book", view_func=BooksAPI.as_view("books_api"), methods=["GET", "POST"])
api_v1.add_url_rule("/book/<int:isbn>/detail", view_func=BookDetailAPI.as_view("book_detail_api"), methods=["GET"])
