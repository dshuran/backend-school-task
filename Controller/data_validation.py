import datetime

from Model.citizen_mdl import unpack_relatives_to_int_list


# Сначала общие валидации конкретного жителя

# Проверка даты на корректность
def validate_date(date_string):
    day, month, year = map(int, date_string.split('.'))
    date = datetime.datetime(year, month, day)
    cur_date = datetime.datetime.today()
    if date > cur_date:
        raise ValueError("Dates are in non-persistent state. Wrong Data")


# Проверка, что в родственниках нет самого себя
def validate_id_not_in_relatives(cit_id, relatives_ids):
    if cit_id in set(relatives_ids):
        raise ValueError("ERROR! Citizen id in relatives")


# Все проверки конкретного жителя в одном месте.
def do_single_citizen_validations(citizen_obj):
    validate_date(citizen_obj['birth_date'])
    validate_id_not_in_relatives(citizen_obj['citizen_id'], citizen_obj['relatives'])

# Дальше идут валидации применительно к POST запросу


# Проверяет на наличие одинаковых id в списке.
def validate_citizens_ids_intersection(citizens):
    users = set()
    for citizen in citizens:
        if citizen.citizen_id in users:
            raise ValueError("Two same ids were found!")
        users.add(citizen.citizen_id)


def validate_relatives(citizens):
    """
    Проверяет, что родственники консистентны по отношению друг к другу.
    Т.е. если А -- родственник Б, то и А должен
    иметь в родственниках Б.

    cit[id] -- интовый set айдишников пользователей.
    cit[id] -- родственники конкретного id
    """
    #
    cit = {}
    for citizen in citizens:
        users = set(unpack_relatives_to_int_list(citizen.relatives))
        cit[citizen.citizen_id] = users
    try:
        for cit_id in cit:
            for relative_id in cit[cit_id]:
                if cit_id not in cit[relative_id]:
                    raise ValueError("Relatives ids are in non-persistent state")
    except KeyError:
        raise KeyError("Trying to use id that doesn't exist as a key")

