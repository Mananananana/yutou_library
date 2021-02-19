def user_schema(user):
    name = user.name
    gender = user.gender.value if user.gender is not None else user.gender
    phone = user.phone
    email = user.email
    register_date = int(user.register_date.timestamp())
    return dict(name=name, gender=gender, phone=phone, email=email, register_date=register_date)
