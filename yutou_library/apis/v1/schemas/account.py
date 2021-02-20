def user_schema(user):
    id = user.id
    selecting_library_id = user.selecting_library_id
    name = user.name
    gender = user.gender.value if user.gender is not None else user.gender
    phone = user.phone
    email = user.email
    register_date = int(user.register_date.timestamp())
    return dict(id=id,
                selecting_library_id=selecting_library_id,
                name=name,
                gender=gender,
                phone=phone,
                email=email,
                register_date=register_date)
