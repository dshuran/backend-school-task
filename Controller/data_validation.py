import datetime



# Сначала общие валидации конкретного жителя

# Проверка даты на корректность
from Model.citizens_relations_mdl import CitizensRelations


def validate_date(date_string):
    # todo: возможно убрать этот try/except
    try:
        day, month, year = map(int, date_string.split('.'))
        date = datetime.datetime(year, month, day)
        cur_date = datetime.datetime.today()
        if date > cur_date:
            raise ValueError("Dates are in non-persistent state. Wrong Data")
    except ValueError as e:
        raise e


# Проверка, что в родственниках нет самого себя
def validate_id_not_in_relatives(cit_id, relatives_ids):
    if cit_id in set(relatives_ids):
        raise ValueError("ERROR! Citizen id in relatives")


# Все проверки конкретного жителя в одном месте.
def do_single_citizen_validations(citizen_obj):
    validate_date(citizen_obj['birth_date'])
    validate_id_not_in_relatives(citizen_obj['citizen_id'], citizen_obj['relatives'])

# Дальше идут валидации применительно к POST запросу


# Проверяет на наличие одинаковых id среди всех жителей.
def validate_citizens_ids_intersection(citizens):
    users = set()
    for citizen in citizens:
        if citizen.citizen_id in users:
            raise ValueError("Two same ids were found!")
        users.add(citizen.citizen_id)


def validate_relatives(citizens, import_id):
    """
    Проверяет, что родственники консистентны по отношению друг к другу.
    Т.е. если А -- родственник Б, то и Б -- родственник А

    Больше информации см. в описании к CitizensRelations
    """
    #
    for citizen in citizens:
        # Получили список всех родственников
        citizen_relations_objects = CitizensRelations.query.filter_by(
            dataset_id=import_id, citizen_id=citizen.citizen_id).all()
        # Для каждого родственника данного жителя пройдемся в цикле.
        for relations_obj in citizen_relations_objects:
            # Получаем id одного из родственников.
            relative_id = relations_obj.relative_id
            # Проверяем, что мы тоже находимся
            # в списке родственников нашего родственника
            relative_relations_obj = CitizensRelations.query.filter_by(
                dataset_id=import_id, citizen_id=relative_id, relative_id=citizen.citizen_id).first()
            if relative_relations_obj is None:
                raise ValueError("Relatives in non-persistent state!")

