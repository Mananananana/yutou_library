def attribute_schema(attribute):
    return {
        "uid": attribute.uid,
        "lid": attribute.lid,
        "rid": attribute.rid,
        "type": attribute.type
    }


def attributes_schema(attributes):
    return {
        "size": len(attributes),
        "members": [attribute_schema(attribute) for attribute in attributes]
    }
