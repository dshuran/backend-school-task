from flask import request, abort, jsonify
from app import Citizen, get_dataset_counter


def main():
    if not request.json:  # more checks
        abort(400)
    citizens = request.json['citizens']
    for citizen_obj in citizens:
        # there check for every citizen obj
        citizen = Citizen(
            citizen_id=citizen_obj['citizen_id'],  # check, что нет такого же айди в выгрузке
            town=citizen_obj['town'],
            street=citizen_obj['street'],
            building=citizen_obj['building'],
            apartment=citizen_obj['apartment'],
            name=citizen_obj['name'],
            birth_date=citizen_obj['birth_date'],
            gender=citizen_obj['gender'],
            relatives=citizen_obj['relatives'])
        # add to db
    dataset_counter = get_dataset_counter()
    success_response = {
        "data": {
            "import_id": dataset_counter.inc()
        }
    }
    return jsonify(success_response), 201
