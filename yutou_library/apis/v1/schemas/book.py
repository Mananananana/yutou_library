def book_schema(book):
    return {
        "id": book.id,
        "lid": book.lid,
        "isbn": book.isbn,
        "status": book.status.value,
        "title": book.title,
        "author": book.author,
        "image_urls": book.image_urls
    }


def books_schema(books):
    return {
        "size": len(books),
        "books": [book_schema(book) for book in books]
    }
