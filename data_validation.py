import datetime
from app import id_separator


def validate_date(date_string):
    day, month, year = map(int, date_string.split('.'))
    datetime.date(year, month, day)


def validate_citizens_ids_intersection(citizens):
    users = set()
    for citizen in citizens:
        if citizen.citizen_id in users:
            raise ValueError
        users.add(citizen.citizen_id)


def validate_id_not_in_relatives(cit_id, relatives_ids):
    if cit_id in set(relatives_ids):
        raise ValueError


def validate_relatives(citizens):
    # cit[id] -> интовый set айдишников пользователей
    cit = {}
    for citizen in citizens:
        users = set()
        if len(citizen.relatives) > 0:
            users = set(map(int, citizen.relatives.split(id_separator)))
        cit[citizen.citizen_id] = users
    try:
        for cit_id in cit:
            for relative_id in cit[cit_id]:
                if cit_id not in cit[relative_id]:
                    raise ValueError
    except KeyError:
        raise

