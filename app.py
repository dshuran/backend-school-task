from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import import_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\MyWorkRep\\backend-school-task\\database.dt'
db = SQLAlchemy(app)

singleton_dataset_counter_id = 1


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
        return 'Dataset %r' % self.id


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
    relatives = db.Column(db.Integer)  # todo Array, or check that everything is ok

    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False, primary_key=True)
    dataset = db.relationship('Dataset', backref=db.backref('citizens'))

    def __repr__(self):
        return 'Citizen %r cit_id %r' % (self.dataset, self.id)


def get_dataset_counter():
    dataset_counter = DatasetCounter.query.filter_by(id=singleton_dataset_counter_id).first()
    if dataset_counter is None:
        dataset_counter = DatasetCounter(id=singleton_dataset_counter_id, counter=0)
        db.session.add(dataset_counter)
        db.session.commit()
    return dataset_counter


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/imports', methods=['POST'])
def do_import_data():
    return import_data.main()


def main():
    # Важно, чтобы создание таблиц
    # происходило после объявления соответствующих классов
    db.create_all()
    # Старт приложения
    app.run(debug=True)


if __name__ == '__main__':
    main()


