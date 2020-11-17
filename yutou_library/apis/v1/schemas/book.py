def book_schema(book):
    bid = book.bid
    lid = book.lid
    isbn = book.isbn
    status = book.status.value
    title = book.title
    author = book.author

    return dict(id=bid,
                lid=lid,
                isbn=isbn,
                status=status,
                title=title,
                author=author)
