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
  carbon_per_capita_0 = db.Column('carbon_per_capita_0', db.Float(precision=10))
  carbon_per_capita_1 = db.Column('carbon_per_capita_1', db.Float(precision=10))
  carbon_per_capita_2 = db.Column('carbon_per_capita_2', db.Float(precision=10))
  
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
  __tablename__ = "food"
  id = db.Column('id', db.Integer, primary_key=True)
  name = db.Column('name', db.String(250))
  carbon_kilos = db.Column('carbon_kilos', db.Float(precision=10))
  image = db.Column('image', db.String(255)) 

  def __init__(self, name, carbon_kilos, image):
    self.name = name
    self.carbon_kilos = carbon_kilos
    self.image = image

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<Food %r>' % (self.id)


class Action(db.Model):
  """ Implements the Action model. """
  __tablename__ = "action"
  id = db.Column('id', db.Integer, primary_key=True)
  user_id = db.Column('user_id', db.Integer, db.ForeignKey("user.id"))
  action_type_id = db.Column('action_type_id', db.Integer, db.ForeignKey("action_type.id"))
  carbon_credit = db.Column('carbon_credit', db.Float(precision=10))
  carbon_debit = db.Column('carbon_debit', db.Float(precision=10))
  created_date = db.Column('created_date', db.DateTime)

  def __init__(self, user_id, action_type_id, carbon_credit, carbon_debit):
    self.user_id = user_id
    self.action_type_id = action_type_id
    self.carbon_credit = carbon_credit
    self.carbon_debit = carbon_debit
    self.created_date = datetime.datetime.utcnow()

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<Action %r>' % (self.id)


class ActionType(db.Model):
  """ Implements the Action Type model. """
  __tablename__ = "action_type"
  id = db.Column('id', db.Integer, primary_key=True)
  description = db.Column('description', db.String(45))

  def __init__(self, description):
    self.description = description

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<Action Type %r>' % (self.id)


class Task(db.Model):
  """ Implements the Task model. """
  __tablename__ = "task"
  id = db.Column('id', db.Integer, primary_key=True)
  user_id = db.Column('user_id', db.Integer)
  task_id = db.Column('task_id', db.Integer)
  status = db.Column('status', db.String(1))
  created_date = db.Column('created_date', db.DateTime)

  def __init__(self, user_id, task_id, status):
    self.user_id = user_id
    self.task_id = task_id
    self.status = status
    self.created_date = datetime.datetime.utcnow()

  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<Task %r>' % (self.id)
