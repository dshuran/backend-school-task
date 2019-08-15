from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\MyWorkRep\\backend-school-task\\database.dt'
db = SQLAlchemy(app)


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    children = db.relationship('Citizen')


class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    dataset = db.relationship('Dataset')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
