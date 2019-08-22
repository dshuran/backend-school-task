from database import db

id_separator = '*'


def pack_relatives_to_db_format(relatives_list):
    """
    Упакуем родственников в необходимый для БД формат.
    В будущем реализация может меняться, нужно будет поменять
    только тело данной функции.
    """
    return id_separator.join(map(str, relatives_list))


def unpack_relatives_to_int_list(db_relatives):
    """
    Распакуем пользователей в лист с переменными типа int.
    Реализация может меняться, при необходимости можно будет
    поменять тело данной функции.
    """
    if len(db_relatives) > 0:
        return list(map(int, db_relatives.split(id_separator)))
    return []


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
    relatives = db.Column(db.String)

    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), primary_key=True)
    # Создаём двухстороннюю ссылку на конкретную выгрузку (dataset)
    dataset = db.relationship('Dataset', backref=db.backref('citizens'))

    def get_relatives_list(self):
        return unpack_relatives_to_int_list(self.relatives)

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
