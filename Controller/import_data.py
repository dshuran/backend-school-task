from flask import request, jsonify
from jsonschema import validate

from Model.citizen_mdl import Citizen, pack_relatives_to_db_format
from Controller.data_validation import validate_relatives, validate_citizens_ids_intersection, \
    do_single_citizen_validations
from database import db
from Model.dataset_counter_mdl import get_dataset_counter
from Model.dataset_mdl import Dataset

# Схема валидации для IMPORT запроса.
import_schema = {
    "type": "object",
    "properties": {
        "citizens": {
            "type": "array",
            "items": {"$ref": "#/definitions/inner_schema"},
            "minItems": 1
        }
    },
    "required": ["citizens"],
    "additionalProperties": False,
    "definitions": {
        "inner_schema": {
            "type": "object",
            "properties": {
                "citizen_id": {
                    "type": "number",
                    "minimum": 0
                },
                "town": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 256
                },
                "street": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 256
                },
                "building": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 256
                },
                "apartment": {
                    "type": "number",
                    "minimum": 0
                },
                "name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 256
                },
                "birth_date": {
                    "type": "string",
                    "pattern": "^\d{2}\.\d{2}\.\d{4}$"
                },
                "gender": {
                    "type": "string",
                    "pattern": "^(male|female)$"
                },
                "relatives": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "uniqueItems": True
                }
            },
            "required": ["citizen_id", "town", "street", "building", "apartment", "name", "birth_date", "gender", "relatives"],
            "additionalProperties": False
        }
    }
}


def main():
    # Пытаемся парсить пришедие данные, как JSON.
    if request.get_json(silent=True) is None:
        # Если не удалось распарсить, выбрасываем исключение.
        raise ValueError("request data can't be parsed as json")
    # Проверяем request.json на соответствие схеме валидации.
    validate(instance=request.json, schema=import_schema)
    citizens = request.json['citizens']
    # Получим счётчик из БД
    dataset_counter = get_dataset_counter()
    # Если будет неудача, то import_id не изменится
    dataset = Dataset(id=(dataset_counter.counter + 1))
    for citizen_obj in citizens:
        # Валидации для одного жителя.
        do_single_citizen_validations(citizen_obj)
        citizen = Citizen(
            citizen_id=citizen_obj['citizen_id'],
            town=citizen_obj['town'],
            street=citizen_obj['street'],
            building=citizen_obj['building'],
            apartment=citizen_obj['apartment'],
            name=citizen_obj['name'],
            birth_date=citizen_obj['birth_date'],
            gender=citizen_obj['gender'],
            relatives=pack_relatives_to_db_format(citizen_obj['relatives']),
            dataset=dataset)
    # Валидации на возможные некорректные данные
    # пользователей в поле relatives
    validate_citizens_ids_intersection(dataset.citizens)
    validate_relatives(dataset.citizens)
    # Данные корректны, добавим в бд.
    # Добавление происходит следующим образом:
    # каждому пользователю сопоставляется
    # конкретный dataset (выгрузка). При условии, что
    # все данные пользователей корректны,
    # мы добавляем данную выгрузку в БД.
    # todo: почекать типы данных: строки/числа
    db.session.add(dataset)
    db.session.commit()
    success_response = {
        "data": {
            "import_id": dataset_counter.inc()
        }
    }
    return jsonify(success_response), 201
