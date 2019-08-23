import names
import datetime

from faker import Faker

fake = Faker()


def get_int(min_len=0, max_len=100000):
    return fake.random_int(min_len, max_len)


def get_street():
    return fake.street_name()


def get_town():
    return fake.city()


def get_gender():
    num = get_int(min_len=1, max_len=2)
    if num == 1:
        return "male"
    else:
        return "female"


def get_name(gender):
    return names.get_full_name(gender)


def get_building_number():
    return fake.building_number()


def get_birth_date():
    day = get_int(1, 25)
    month = get_int(1, 12)
    year = get_int(1980, 2000)
    date = datetime.datetime(year, month, day)
    return date.strftime('%d.%m.%Y')


def get_correct_citizen():
    citizen_gender = get_gender()
    citizen = {
        "citizen_id": get_int(),
        "town": get_town(),
        "street": get_street(),
        "building": get_building_number(),
        "apartment": get_int(1, 1000),
        "name": get_name(citizen_gender),
        "birth_date": get_birth_date(),
        "gender": citizen_gender,
        "relatives": []
    }
    return citizen

# todo: сделать incorrent citizen


def main():
    for i in range(2):
        print(get_correct_citizen())


if __name__ == '__main__':
    main()
