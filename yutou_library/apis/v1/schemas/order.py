def order_schema(order):
    return {
        "id": order.id,
        "uid": order.uid,
        "bid": order.bid,
        "effective_date": order.effective_date,
        "invalid_date": order.invalid_date
    }


def orders_schema(orders):
    return {
        "size": len(orders),
        "orders": [order_schema(order) for order in orders]
    }
