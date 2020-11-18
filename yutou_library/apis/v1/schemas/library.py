def library_schema(library):
    id = library.id
    name = library.name
    status = library.status.value
    create_date = int(library.create_date.timestamp())
    return dict(id=id, name=name,
                status=status, create_date=create_date)


def libraries_schema(attributes):
    size = len(attributes)
    return {
        "size": size,
        "libraries": [library_schema(attribute.library) for attribute in attributes]
    }
