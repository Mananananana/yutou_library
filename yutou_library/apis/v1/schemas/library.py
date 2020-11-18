def library_schema(library):
    id = library.id
    name = library.name
    status = library.status.value
    create_date = int(library.create_date.timestamp())
    return dict(id=id, name=name,
                status=status, create_date=create_date)
