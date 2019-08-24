from database import db


class CitizensRelations(db.Model):
    """
    Таблица, которая хранит записи о родственниках данного пользователя.
    Происходит это следующим образом: зная dataset_id (номер выгрузки) и
    relative_id (id родственника), мы можем получить список всех родственников
    данного жителя из базы данных.

    Для того, чтобы проверить наличие двухсторонней между двумя жителями,
    достаточно наличие двух записей в таблице:
    1. (dataset_id, citizen_id, relative_id)
    2. (dataset_id, relative_id, citizen_id)
    """
    dataset_id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.Integer, primary_key=True)
    relative_id = db.Column(db.Integer, primary_key=True)
