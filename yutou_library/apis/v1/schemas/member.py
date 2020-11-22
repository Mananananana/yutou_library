def attribute_schema(attribute):
    return {
        "uid": attribute.uid,
        "level": attribute.level.value,
        "status": attribute.status.value,
        "type": attribute.type
    }


def attributes_schema(attributes):
    return {
        "size": len(attributes),
        "members": [attribute_schema(attribute) for attribute in attributes]
    }
