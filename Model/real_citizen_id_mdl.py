from database import db


def get_real_id(dataset_id, citizen_id):
    real_id = RealCitizenId.query.filter_by(dataset_id=dataset_id, citizen_id=citizen_id).first()
    if real_id is None:
        raise ValueError('Cannot find a real id for this combination!')
    return real_id


class RealCitizenId(db.Model):
    dataset_id = db.Column(db.Integer)
    citizen_id = db.Column(db.Integer)
    real_id = db.Column(db.Integer)
