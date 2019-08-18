from database import db

id_separator = '*'

class Citizen(db.Model):
    # some checks on date maybe
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
    dataset = db.relationship('Dataset', backref=db.backref('citizens'))

    def get_relatives_list(self):
        relatives_list = []
        if len(self.relatives) > 0:
            relatives_list = list(map(int, self.relatives.split(id_separator)))
        return relatives_list

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