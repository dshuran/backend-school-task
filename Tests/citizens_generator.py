import json
import random

import names
import datetime

from faker import Faker
from flask import jsonify

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


def fill_list_with_relatives(citizens, citizens_ids):
    # id -> список айдишников родственников
    citizen_relatives = {}
    for cit_id in citizens:
        relatives_amount = get_int(0, len(citizens_ids) - 1)
        print('amount = ', relatives_amount)
        citizens_pull = set(citizens_ids)
        citizens_pull.remove(cit_id)
        for i in range(relatives_amount):
            random_id = random.choice(tuple(citizens_pull))
            citizens_pull.remove(random_id)
            if cit_id not in citizens[random_id]['relatives']:
                citizens[random_id]['relatives'].append(cit_id)
            if random_id not in citizens[cit_id]['relatives']:
                citizens[cit_id]['relatives'].append(random_id)


def get_random_post_data(citizens_amount):
    citizens = {}
    for i in range(citizens_amount):
        citizen = get_correct_citizen()
        citizens[citizen['citizen_id']] = citizen
    citizens_ids = []
    for cit_id in citizens:
        citizens_ids.append(cit_id)
    fill_list_with_relatives(citizens=citizens, citizens_ids=citizens_ids)
    citizens_list = []
    for cit_id in citizens:
        citizens_list.append(citizens[cit_id])
    res = {
        "citizens": citizens_list
    }
    return json.dumps(res)


def main():
    print(get_random_post_data(4))


if __name__ == '__main__':
    main()
