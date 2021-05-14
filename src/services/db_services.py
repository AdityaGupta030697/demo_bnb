from data.owners import Owner


def create_account(name: str, email: str, age: int,
                   phone: str, gender: str) -> Owner:
    owner = Owner()
    owner.first_name = name.split(" ")[0]
    owner.last_name = name.split(" ")[1]
    owner.email = email
    owner.age = age
    owner.phone_number = phone
    owner.gender = gender
    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    return Owner.objects(email=email).first()
