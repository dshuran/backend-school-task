from flask import jsonify, abort
from dataset_mdl import Dataset


def main(import_id):
    # Пытаемся получить выгрузку по её id.
    dataset = Dataset.query.filter_by(id=import_id).first()
    if dataset is None:
        # Не получили -- выбрасываем исключение
        raise ValueError("There is no dataset with that id")
    else:
        res_list = []
        for citizen in dataset.citizens:
            res_list.append(citizen.json_representation())
        res = {
            "data": res_list
        }
        # todo: вывод без переводов строки. Скорее всего уберётся в production-версии.
        return jsonify(res), 200
