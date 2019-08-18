from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\MyWorkRep\\backend-school-task\\database.dt'
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

singleton_dataset_id = 1
id_separator = '*'


class DatasetCounter(db.Model):
    # SINGLETON
    id = db.Column(db.Integer, primary_key=True) # Всегда должен быть = 1
    counter = db.Column(db.Integer, nullable=False)

    def inc(self):
        self.counter += 1
        db.session.commit()
        return self.counter

    def __repr__(self):
        return 'Import Counter id = %r counter = %r' % (self.id, self.counter)


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return 'Dataset %r: %r' % (self.id, self.citizens)


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


def get_dataset_counter():
    dataset_counter = DatasetCounter.query.filter_by(id=singleton_dataset_id).first()
    if dataset_counter is None:
        dataset_counter = DatasetCounter(id=singleton_dataset_id, counter=0)
        db.session.add(dataset_counter)
        db.session.commit()
    return dataset_counter


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/imports', methods=['POST'])
def do_import_data():
    import import_data
    return import_data.main()


@app.route('/imports/<import_id>/citizens', methods=['GET'])
def do_get_data(import_id):
    import get_data
    return get_data.main(import_id)


def main():
    # Важно, чтобы создание таблиц
    # происходило после объявления соответствующих классов
    # todo: Убрать в продакшене.
    db.create_all()
    # Старт приложения
    app.run(debug=True)


if __name__ == '__main__':
    main()


