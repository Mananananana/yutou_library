def borrow_schema(borrow):
    return_date = borrow.return_date
    if return_date is not None:
        return_date = int(return_date.timestamp())
    return {
        "lid": borrow.lid,
        "bid": borrow.bid,
        "borrow_date": int(borrow.borrow_date.timestamp()),
        "return_date": return_date
    }


def borrows_schema(borrows):
    return {
        "size": len(borrows),
        "borrows": [borrow_schema(borrow) for borrow in borrows]
    }
