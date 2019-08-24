from Model.citizens_relations_mdl import CitizensRelations
from database import db


def get_relatives_as_int_list(citizen_id, dataset_id):
    """
    Распакуем жителей в лист с переменными типа int, где
    значение - id жителя.
    Реализация может меняться, при необходимости можно будет
    поменять тело данной функции.

    Более подробную документацию см.
    в описании к CitizensRelations.
    """
    citizen_relations_objects = CitizensRelations.query.filter_by(
        dataset_id=dataset_id, citizen_id=citizen_id).all()
    relatives_list = []
    for relations_obj in citizen_relations_objects:
        relatives_list.append(relations_obj.relative_id)
    return relatives_list


class Citizen(db.Model):
    """
    Основной класс жителя. Primary Key является составным и
    зависит от citizen_id и dataset_id.
    """
    citizen_id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String)
    street = db.Column(db.String)
    building = db.Column(db.String)
    apartment = db.Column(db.Integer)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    gender = db.Column(db.String)

    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), primary_key=True)
    # Создаём двухстороннюю ссылку на конкретную выгрузку (dataset)
    dataset = db.relationship('Dataset', backref=db.backref('citizens'))

    def get_relatives_list(self):
        return get_relatives_as_int_list(citizen_id=self.citizen_id, dataset_id=self.dataset_id)

    def json_representation(self):
        relatives_list = self.get_relatives_list()
        res = {
            "citizen_id": self.citizen_id,
            "town": self.town,
            "street": self.street,
            "building": self.building,
            "apartment": self.apartment,
            "name": self.name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "relatives": relatives_list
        }
        return res

    def __repr__(self):
        return 'Citizen %r cit_id %r' % (self.dataset, self.citizen_id)
