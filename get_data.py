from app import Dataset
from flask import jsonify, Response


def main(import_id):
    dataset = Dataset.query.filter_by(id=import_id).first()
    if dataset is None:
        raise ValueError
    else:
        res_list = []
        for citizen in dataset.citizens:
            res_list.append(citizen.json_representation())
        res = {
            "data": res_list
        }
        return res, 200
