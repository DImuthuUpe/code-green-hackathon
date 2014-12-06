from server import db
import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column('id',db.Integer , primary_key=True)
    country_id = db.Column('country_id', db.Integer)
    status = db.Column('status' , db.Integer)
    miles_per_day = db.Column('miles_per_day' , db.Integer)
    registration = db.Column('registration' , db.String(45))
    created_date = db.Column('created_date',db.DateTime)

    def __init__(self , country_id ,status, miles_per_day , registration ):
        self.country_id = country_id
        self.status = status
        self.miles_per_day = miles_per_day
        self.registration = registration
        self.created_date = datetime.datetime.utcnow()

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.id)