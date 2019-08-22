from citizen_mdl import Citizen
from dataset_mdl import Dataset


def get_month_from_date(date_string):
    day, month, year = map(int, date_string.split('.'))
    assert isinstance(month, int)
    return month


# Получим месяц рождения жителя в диапазоне
# от 1 до 12, используя его id.
def get_birthday_month(relative_id, import_id):
    relative = Citizen.query.filter_by(citizen_id=relative_id, dataset_id=import_id).first()
    if relative is None:
        raise ValueError("relative is None!")
    else:
        return get_month_from_date(relative.birth_date)


def main(import_id):
    dataset = Dataset.query.filter_by(id=import_id).first()
    citizens = dataset.citizens
    presents_number = []
    for i in range(13):
        presents_number.append({})
    for citizen in citizens:
        # todo: в остальных местах такую же конструкцию с get_relatives_list
        relatives_list = citizen.get_relatives_list()
        for relative_id in relatives_list:
            assert isinstance(relative_id, int)
            month = get_birthday_month(relative_id, import_id)
            assert isinstance(month, int)
            if citizen.citizen_id in presents_number[month]:
                presents_number[month][citizen.citizen_id] += 1
            else:
                presents_number[month][citizen.citizen_id] = 1
    # Словарь: "номер от 1 до 12": лист с объектами
    # todo: Больше документации
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
    final_output = {
        "data": res
    }
    return final_output, 200

