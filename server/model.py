""" Implements the data models. """

from server import db
import datetime

class User(db.Model):
  """ Implements the User model. """
  __tablename__ = "user"
  id = db.Column('id', db.Integer, primary_key=True)
  country_id = db.Column('country_id', db.Integer)
  status = db.Column('status', db.Integer)
  miles_per_day = db.Column('miles_per_day', db.Integer)
  registration = db.Column('registration', db.String(45))
  created_date = db.Column('created_date', db.DateTime)

  def __init__(self, country_id, status, miles_per_day, registration):
    self.country_id = country_id
    self.status = status
    self.miles_per_day = miles_per_day
    self.registration = registration
    self.created_date = datetime.datetime.utcnow()

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<User %r>' % (self.id)
  

class Country(db.Model):
  """ Implements the Country model. """
  __tablename__ = "country"
  id = db.Column('id', db.Integer, primary_key=True)
  name = db.Column('name', db.String(65))
  population = db.Column('population', db.Integer)
  carbon_per_capita_0 = db.Column('carbon_per_capita_0', db.Float(precision=2))
  carbon_per_capita_1 = db.Column('carbon_per_capita_1', db.Float(precision=2))
  carbon_per_capita_2 = db.Column('carbon_per_capita_2', db.Float(precision=2))
  
  def __init__(self, name, popultion, carbon_per_capita_0, carbon_per_capita_1, carbon_per_capita_2):
    self.name = name
    self.population = population
    self.carbon_per_capita_0 = carbon_per_capita_0
    self.carbon_per_capita_1 = carbon_per_capita_1
    self.carbon_per_capita_2 = carbon_per_capita_2

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<Country %r>' % (self.id)


class Food(db.Model):
  """ Implements the Food model. """
  pass


class Action(db.Model):
  """ Implements the Action model. """
  pass
