from flask import jsonify

from Model.citizen_mdl import Citizen
from Model.dataset_mdl import Dataset


# Получает месяц типа int из строковой даты
def get_month_from_date(date_string):
    day, month, year = map(int, date_string.split('.'))
    assert isinstance(month, int)
    return month


# Получим месяц рождения жителя в диапазоне
# от 1 до 12, используя его id, тип int
def get_birthday_month(relative_id, citizens_birth_dates):
    return get_month_from_date(citizens_birth_dates[relative_id])


def main(import_id):
    """
    dataset - одна из выгрузок.

    citizens - жители, которые были перечислены в
    конкретной выгрузке с id = import_id

    presents_number - лист из 13 элементов, каждый из которых содержит словарь.
    presents_number[month][citizen_id] - кол-во подарков, которые житель с id = citizen_id
    будет покупать в месяце month.

    Каждый из соовтетствующих словарей внутри presents_number имеет следующую структуру:
    Ключ: id жителя.
    Значение: кол-во подарков (см. описание presents_number выше).

    res - словарь, необходимый для вывода информации в соответствующем формате.
    Если в данном месяце нет жителей, которые будут покупать подарки, то значением ключа
    является пустой массив (пример: res[month] = []). Если же жители, которые соберутся
    в магазин за подарками присутствуют, значением является res_atom -- структура, содержащая
    в себе citizen_id - id жителя и presents - кол-во подарков

    """
    dataset = Dataset.query.filter_by(id=import_id).first()
    citizens = dataset.citizens
    # id - "дата рождения"
    citizens_births_dates = {}
    for citizen in citizens:
        citizens_births_dates[citizen.citizen_id] = citizen.birth_date
    # Документация по presents_number выше.
    presents_number = []
    for i in range(13):
        presents_number.append({})
    for citizen in citizens:
        print(citizen.citizen_id)
        # todo: в остальных местах такую же конструкцию с get_relatives_list
        relatives_list = citizen.get_relatives_list()
        for relative_id in relatives_list:
            assert isinstance(relative_id, int)
            month = get_birthday_month(relative_id, citizens_births_dates)
            assert isinstance(month, int)
            if citizen.citizen_id in presents_number[month]:
                presents_number[month][citizen.citizen_id] += 1
            else:
                presents_number[month][citizen.citizen_id] = 1
    print('THERE')
    # См. документацию выше по res.
    res = {}
    for month in range(1, 12 + 1):
        if len(presents_number[month]) == 0:
            res[month] = []
        else:
            for citizen_id in presents_number[month]:
                if month not in res:
                    res[month] = []
                res_atom = {
                    "citizen_id": citizen_id,
                    "presents": presents_number[month][citizen_id]
                }
                res[month].append(res_atom)
    # Финальный словарь, который будем выводить.
    final_output = {
        "data": res
    }
    return jsonify(final_output), 200
