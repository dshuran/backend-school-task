from flask import request, jsonify
from jsonschema import validate

from Model.citizen_mdl import Citizen
from Controller.data_validation import validate_date, validate_id_not_in_relatives
from Model.citizens_relations_mdl import CitizensRelations
from database import db

# Схема валидации для PATCH запроса
dataset_patch_schema = {
    "type": "object",
    "properties": {
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
    "anyOf": [
        {"required": ["town"]},
        {"required": ["street"]},
        {"required": ["building"]},
        {"required": ["apartment"]},
        {"required": ["name"]},
        {"required": ["birth_date"]},
        {"required": ["gender"]},
        {"required": ["relatives"]}
    ],
    "additionalProperties": False,

}


# Удаляет citizen_id из списка родственников пользователя с id = relative_id
def remove_citizen_from_relative_list(relative_id, citizen_id, import_id):
    relative_relations_obj = CitizensRelations.query.filter_by(
        dataset_id=import_id, citizen_id=relative_id, relative_id=citizen_id).first()
    if relative_relations_obj is None:
        raise ValueError("Cannot find suck relations object!")
    else:
        db.session.delete(relative_relations_obj)


# Добавляет в список родственников пользователя
# с id = relative_id пользователя citizen_id
def add_citizen_to_relative_list(relative_id, citizen_id, import_id):
    relative_relations_obj = CitizensRelations(dataset_id=import_id, citizen_id=relative_id, relative_id=citizen_id)
    db.session.add(relative_relations_obj)


def main(import_id, citizen_id):
    # Пытаемся парсить пришедие данные, как JSON.
    if request.get_json(silent=True) is None:
        # Если не удалось распарсить, выбрасываем исключение.
        raise ValueError("request data can't be parsed as json")
    # Получаем соответствующего жителя по двум
    # основным ключам -- номеру выгрузки и id.
    citizen = Citizen.query.filter_by(citizen_id=citizen_id, dataset_id=import_id).first()
    if citizen is None:
        # Если не нашли такого пользователя, выбрасываем исключение.
        raise ValueError("Citizen with such citizen_id and import_id wasn't found")
    else:
        citizen_obj = request.json
        # Общая валидация PATCH-схемы.
        validate(instance=citizen_obj, schema=dataset_patch_schema)
        # Валидация отдельных полей. Проще сделать её вручную.
        if 'birth_date' in citizen_obj:
            validate_date(citizen_obj['birth_date'])
        if 'relatives' in citizen_obj:
            validate_id_not_in_relatives(citizen.citizen_id, citizen_obj['relatives'])
        # Валидация закончена
        if 'town' in citizen_obj:
            citizen.town = citizen_obj['town']
        if 'street' in citizen_obj:
            citizen.street = citizen_obj['street']
        if 'building' in citizen_obj:
            citizen.building = citizen_obj['building']
        if 'apartment' in citizen_obj:
            citizen.apartment = citizen_obj['apartment']
        if 'name' in citizen_obj:
            citizen.name = citizen_obj['name']
        if 'birth_date' in citizen_obj:
            citizen.birth_date = citizen_obj['birth_date']
        if 'gender' in citizen_obj:
            citizen.gender = citizen_obj['gender']
        if 'relatives' in citizen_obj:
            # Получим два сета с id пользователей
            prev_relatives_list = citizen.get_relatives_list()
            cur_relatives_list = citizen_obj['relatives']
            prev_relatives = set(prev_relatives_list)
            cur_relatives = set(cur_relatives_list)
            # Получим разницу в обоих случаях и
            # удалим/добавим необходимые записи для
            # жителя и его родственника.
            for relative_id in prev_relatives.difference(cur_relatives):
                remove_citizen_from_relative_list(relative_id=relative_id, citizen_id=citizen_id, import_id=import_id)
                remove_citizen_from_relative_list(relative_id=citizen_id, citizen_id=relative_id, import_id=import_id)
            for relative_id in cur_relatives.difference(prev_relatives):
                add_citizen_to_relative_list(relative_id=relative_id, citizen_id=citizen_id, import_id=import_id)
                add_citizen_to_relative_list(relative_id=citizen_id, citizen_id=relative_id, import_id=import_id)
        # Добавим в базу данных.
        db.session.commit()
        res = {
            "data": citizen.json_representation()
        }
        return jsonify(res), 200


