""" Handles REST calls from app and dashboard. 

Routes:
  /register: 
    Requires the country ID.
    
  /ping/<cookie>:
    Requires the user cookie.
    
  /countries:
    Requires no parameters.
    
  /foods:
    Requires no parameters.
    
  /food_choice:
    Requires the user cookie and a food ID.
    Example Response:
      { "score" : "-100" }
    Example Error:
      { "error" : "True" }

  /stats:
    Requires the user cookie.
    Example Response:
      {
        "credit_trend": null,
        "debit_trend": null,
        "total_credit": 0,
        "total_debit": -9,
        "target": "0.041"
      }
    and 
      {
        "credit_trend": "down",
        "debit_trend": "up",
        "total_credit": -1,
        "total_debit": 11,
        "target": "0.041"
      }
      
  /user_time_series:
    Requires the user cookie.
    Example Response:
      {
        "credit": 
          [{"date": "2014-12-08", "value": 6.0}, {"date": "2014-12-07", "value": 0.0}, {"date": "2014-12-06", "value": 0.0}, {"date": "2014-12-05", "value": 56.0}, {"date": "2014-12-04", "value": 0.0}, {"date": "2014-12-03", "value": 6.0}, {"date": "2014-12-02", "value": 3.0}, {"date": "2014-12-01", "value": 3.0}, {"date": "2014-11-29", "value": 35.0}], 
        "debit": 
          [{"date": "2014-12-08", "value": 60.0}, {"date": "2014-12-07", "value": 20.0}, {"date": "2014-12-06", "value": 20.0}, {"date": "2014-12-05", "value": 0.0}, {"date": "2014-12-04", "value": 20.0}, {"date": "2014-12-03", "value": 0.0}, {"date": "2014-12-02", "value": 0.0}, {"date": "2014-12-01", "value": 12.0}, {"date": "2014-11-29", "value": 30.0}]
      }
      
  /country_time_series:
    Requires the user cookie.
    Example Response:
      { 
        "credit": 
          [{"date": "2014-11-29", "value": 35.0}, {"date": "2014-11-30", "value": 23.0}, {"date": "2014-12-01", "value": 3.0}, {"date": "2014-12-02", "value": 3.0}, {"date": "2014-12-03", "value": 6.0}, {"date": "2014-12-04", "value": 27.0}, {"date": "2014-12-05", "value": 56.0}, {"date": "2014-12-06", "value": 100.0}, {"date": "2014-12-07", "value": 0.0}, {"date": "2014-12-08", "value": 22.0}],          
        "debit": 
          [{"date": "2014-11-29", "value": 60.0}, {"date": "2014-11-30", "value": 0.0}, {"date": "2014-12-01", "value": 65.0}, {"date": "2014-12-02", "value": 0.0}, {"date": "2014-12-03", "value": 5.0}, {"date": "2014-12-04", "value": 43.0}, {"date": "2014-12-05", "value": 7.0}, {"date": "2014-12-06", "value": 20.0}, {"date": "2014-12-07", "value": 43.0}, {"date": "2014-12-08", "value": 60.0}]
      }
  /add_task:
    Requires user cookie, ...
"""


import datetime
import uuid
import json

from flask import Flask, render_template, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import cross_origin
from sqlalchemy import text
from sqlalchemy.sql import func

from model import *
from db_utils import *

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/puppy-earth'
app.config['CORS_HEADERS'] = "Content-Type"
app.debug = True

db = SQLAlchemy(app)


@app.route('/ping/<cookie>')
@cross_origin()
def ping(cookie):
    try:
      result = { 'id': User.query.filter_by(registration=cookie).first().id }
    except:
      result = {}
    return Response(json.dumps(result), mimetype='application/json')
    
@app.route('/countries')
@cross_origin()
def countries():
    countries = []
    country_list = Country.query.all()
    for country in country_list:
      countries.append({'id': country.id, 'name': country.name})
    return Response(json.dumps(countries), mimetype='application/json')

@app.route('/foods')
@cross_origin()
def foods():
    foods = []
    
    sql = 'select id, name, image from food where carbon_kilos <= 10 order by rand() limit 1'
    foods.extend(run_query(db, sql, multi=True))

    sql = 'select id, name, image from food where carbon_kilos > 10 and carbon_kilos <=20 order by rand() limit 2'
    foods.extend(run_query(db, sql, multi=True))

    sql = 'select id, name, image from food where carbon_kilos > 20 order by rand() limit 1'
    foods.extend(run_query(db, sql, multi=True))

    return Response(json.dumps(foods, default=decimal_default), mimetype='application/json')

@app.route('/food_choice', methods=['POST'])
@cross_origin()
def add_food_choice():
    user_data = json.loads(request.data)
    user_registration = user_data['registration']
    food_id = user_data['food_id']

    user_id = User.query.filter_by(registration=user_registration).first().id

    try:
      food_carbon = Food.query.get(int(food_id)).carbon_kilos
    except:
      food_carbon = 0
    
    sql = "select avg(carbon_kilos) from food"
    results = run_query(db, sql)
    if len(results) > 0:
      average = results[0]['avg(carbon_kilos)']
    else:
      average = 0
    
    score = int(food_carbon - average)
    if score > 0:
      debit = score
      credit = 0
    else:
      debit = 0
      credit = score

    action = Action(int(user_id), 1, debit, credit)
    try:
        db.session.add(action)
        db.session.flush()
        db.session.commit()
        response = {'score': score}
    except:
        db.session.rollback()
        response = {'error': True}
    
    return Response(json.dumps(response), mimetype='application/json')

@app.route('/add_task', methods=['POST'])
@cross_origin()
def add_task():
    user_data = json.loads(request.data)
    user_registration = user_data['registration']
    # Other request fields to be parsed here.
    
    user = User.query.filter_by(registration=user_registration).first()
    
    # TODO
    
    # task = Task(int(user_id), text, carbon_credit, carbon_debit)
    # try:
    #     db.session.add(task)
    #     db.session.flush()
    #     db.session.commit()
    #     response = {}
    # except:
    #     db.session.rollback()
    #     response = {}
    
    # return Response(json.dumps(response), mimetype='application/json')
    
@app.route('/stats', methods=['GET'])
@cross_origin()
def stats():
    user_registration = request.args.get('registration')
    user = User.query.filter_by(registration=user_registration).first()
    
    # Retrieve totals.
    total_credit = 0
    total_debit = 0
    total_credit_list = Action.query.with_entities(func.sum(Action.carbon_credit).label('total_credit')).filter_by(user_id=user.id).first()
    total_debit_list = Action.query.with_entities(func.sum(Action.carbon_debit).label('total_debit')).filter_by(user_id=user.id).first()
    if len(total_credit_list) > 0:
      total_credit = total_credit_list[0]
    if len(total_debit_list) > 0:
      total_debit = total_debit_list[0]

    # Calculate trends.
    credit_trend = None
    debit_trend = None
    credit_rows = Action.query.filter_by(user_id=user.id).order_by(Action.created_date.desc()).limit(2).all()
    debit_rows = Action.query.filter_by(user_id=user.id).order_by(Action.created_date.desc()).limit(2).all()
    if len(credit_rows) == 2:
      credit_trend = 'up' if credit_rows[0] < credit_rows[1] else 'down'
    if len(debit_rows) == 2:
      debit_trend = 'up' if debit_rows[0] > debit_rows[1] else 'down'

    # Calculate target.      
    current_day_of_year = datetime.datetime.now().timetuple().tm_yday
    registration_day_of_the_year = user.created_date.timetuple().tm_yday
    target_days = 1 if (current_day_of_year - registration_day_of_the_year == 0) else current_day_of_year - registration_day_of_the_year
    carbon_per_capita = Country.query.get(int(user.country_id)).carbon_per_capita_0
    carbon_per_capita_per_day = carbon_per_capita / 365
    target = target_days * float(carbon_per_capita_per_day) * 0.8 * 1000
    
    response = {
      'total_credit': total_credit,
      'total_debit': total_debit,
      'credit_trend': credit_trend,
      'debit_trend': debit_trend,
      'target': '{0:.3f}'.format(target)
    }
    
    return Response(json.dumps(response, default=decimal_default), mimetype='application/json')

@app.route('/user_time_series', methods=['GET'])
@cross_origin()
def user_time_series():
    user_registration = request.args.get('registration')
    user = User.query.filter_by(registration=user_registration).first()
    
    response = {
      'credit': [],
      'debit': []
    }
    
    summed_credits = Action.query.\
      with_entities(Action.created_date, func.sum(Action.carbon_credit.label('total_credit'))).\
      filter_by(user_id=user.id).\
      group_by(Action.created_date).\
      order_by(Action.created_date.desc()).limit(1000).all()
    for row in summed_credits:
      response['credit'].append({'date': '{0}'.format(row[0]), 'value': row[1]})

    summed_debits = Action.query.\
      with_entities(Action.created_date, func.sum(Action.carbon_debit.label('total_debit'))).\
      filter_by(user_id=user.id).\
      group_by(Action.created_date).\
      order_by(Action.created_date.desc()).limit(1000).all()
    for row in summed_debits:
      response['debit'].append({'date': '{0}'.format(row[0]), 'value': row[1]})

    return Response(json.dumps(response, default=decimal_default), mimetype='application/json')

@app.route('/country_time_series', methods=['GET'])
@cross_origin()
def country_time_series():
    user_registration = request.args.get('registration')
    user = User.query.filter_by(registration=user_registration).first()

    response = {
      'credit': [],
      'debit': []
    }

    summed_credits = Action.query.with_entities(Action.created_date, func.sum(Action.carbon_credit.label('total_credit'))).\
      join(User, User.id == Action.user_id).\
      group_by(Action.created_date, User.country_id).\
      filter_by(country_id=user.country_id).\
      limit(1000).all()
    for row in summed_credits:
      response['credit'].append({'date': '{0}'.format(row[0]), 'value': row[1]})
      
    summed_debits = Action.query.with_entities(Action.created_date, func.sum(Action.carbon_debit.label('total_debit'))).\
      join(User, User.id == Action.user_id).\
      group_by(Action.created_date, User.country_id).\
      limit(1000).all()
    for row in summed_debits:
      response['debit'].append({'date': '{0}'.format(row[0]), 'value': row[1]})

    return Response(json.dumps(response, default=decimal_default), mimetype='application/json')

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    cookie = str(uuid.uuid4())
    user_data = json.loads(request.data)
    country_id = user_data['country']

    response = {}
    user = User(int(country_id), 0, 0, cookie)
    try:
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        response = { 'cookie': cookie }
    except:
        db.session.rollback()
        response = {'cookie': ''}
        
    return Response(json.dumps(response), mimetype='application/json')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, threaded=True)
