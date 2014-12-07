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
      
  /add_task:
    Requires user cookie, ...

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
      
  /user_actions:
    Requires the user cookie.
    Example Response:
      {"actions": [{"action": "Food", "count": 5}, {"action": "Travel", "count": 7}, {"action": "Household", "count": 4}]}
      
  /country_time_series:
    Requires the user cookie.
    Example Response:
      { 
        "credit": 
          [{"date": "2014-11-29", "value": 35.0}, {"date": "2014-11-30", "value": 23.0}, {"date": "2014-12-01", "value": 3.0}, {"date": "2014-12-02", "value": 3.0}, {"date": "2014-12-03", "value": 6.0}, {"date": "2014-12-04", "value": 27.0}, {"date": "2014-12-05", "value": 56.0}, {"date": "2014-12-06", "value": 100.0}, {"date": "2014-12-07", "value": 0.0}, {"date": "2014-12-08", "value": 22.0}],          
        "debit": 
          [{"date": "2014-11-29", "value": 60.0}, {"date": "2014-11-30", "value": 0.0}, {"date": "2014-12-01", "value": 65.0}, {"date": "2014-12-02", "value": 0.0}, {"date": "2014-12-03", "value": 5.0}, {"date": "2014-12-04", "value": 43.0}, {"date": "2014-12-05", "value": 7.0}, {"date": "2014-12-06", "value": 20.0}, {"date": "2014-12-07", "value": 43.0}, {"date": "2014-12-08", "value": 60.0}]
      }
  
  /top_countries:
    Requires no parameters.
    Example Response:
      {
        "savings": 
          [{"country": "United States", "savings": 14.333333333333334, "ratio": 1.2976744186046512, "emissions": 18.6}, {"country": "Aruba", "savings": 0, "ratio": 22.58, "emissions": 22.58}, {"country": "Andorra", "savings": 0, "ratio": 6.74, "emissions": 6.74}, {"country": "Afghanistan", "savings": 0, "ratio": 0.15, "emissions": 0.15}, {"country": "Angola", "savings": 0, "ratio": 1.45, "emissions": 1.45}, {"country": "Albania", "savings": 0, "ratio": 1.42, "emissions": 1.42}, {"country": "Arab World", "savings": 0, "ratio": 4.44, "emissions": 4.44}, {"country": "United Arab Emirates", "savings": 0, "ratio": 23.38, "emissions": 23.38}, {"country": "Argentina", "savings": 0, "ratio": 4.79, "emissions": 4.79}, {"country": "Armenia", "savings": 0, "ratio": 1.87, "emissions": 1.87}], 
        "ratios": 
          [{"country": "Lesotho", "savings": 0, "ratio": 0.01, "emissions": 0.01}, {"country": "Burundi", "savings": 0, "ratio": 0.03, "emissions": 0.03}, {"country": "Mali", "savings": 0, "ratio": 0.05, "emissions": 0.05}, {"country": "Rwanda", "savings": 0, "ratio": 0.05, "emissions": 0.05}, {"country": "Chad", "savings": 0, "ratio": 0.05, "emissions": 0.05}, {"country": "Congo, Dem. Rep.", "savings": 0, "ratio": 0.05, "emissions": 0.05}, {"country": "Central African Republic", "savings": 0, "ratio": 0.06, "emissions": 0.06}, {"country": "Niger", "savings": 0, "ratio": 0.06, "emissions": 0.06}, {"country": "Somalia", "savings": 0, "ratio": 0.07, "emissions": 0.07}, {"country": "Eritrea", "savings": 0, "ratio": 0.08, "emissions": 0.08}]
      }      
  
  /user
  Requires the user cookie
  Example Response
    {
      "total_points": -88
      "total_tasks": 1
    }
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
from random import randint

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
    country_id = User.query.filter_by(registration=user_registration).first().country_id
    
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
    
    score = int(average-food_carbon)
    if(score==0):
        score=1
        
    if score < 0:
      debit = abs(score)
      credit = 0
      assign_task(user_id) # New task is assigned because of negative score
    else:
      debit = 0
      credit = abs(score)
    
    sql = "select name from country where id="+str(country_id);
    results = run_query(db, sql);
    country_name= results[0]['name']
    
    response = {'score': score,'country':country_name}
    action = Action(int(user_id), 1, credit, debit)
    try:
        db.session.add(action)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()

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
    
@app.route('/user_actions', methods=['GET'])
@cross_origin()
def user_actions():
    user_registration = request.args.get('registration')
    user = User.query.filter_by(registration=user_registration).first()
    
    number_to_string = {'1': 'Food', '2': 'Travel', '3': 'Household'}
    response = {'actions': []}
    
    actions = Action.query.with_entities(Action.action_type_id, func.count(Action.id)).filter_by(user_id=user.id).group_by(Action.action_type_id).all()
    for action in actions:
      response['actions'].append({'action': number_to_string[str(action[0])], 'count': action[1]})
    
    return Response(json.dumps(response), mimetype='application/json')

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

@app.route('/top_countries', methods=['GET'])                                                                                                                           
@cross_origin()                                                                                                                                                         
def top_countries():
    country_list = []
    country_stats = {}
    countries = Country.query.all()
    for country in countries:
      sql = "select user_id, sum(carbon_credit)-sum(carbon_debit) as savings from action " \
        "join user on user.id = action.user_id where user.country_id = " + str(country.id) + " group by user_id;"
      results = run_query(db, sql)
      
      if country.carbon_per_capita_0 < 0:
        continue
      
      avg_savings = 0
      if len(results) > 0:
        num_users = 0
        for row in results:
          num_users += 1
          avg_savings += row["savings"] if row["savings"] > 0 else 0
        avg_savings /= num_users if num_users > 0 else 0

      country_stats["country"] = country.name
      country_stats["savings"] = avg_savings if avg_savings > 0 else 0
      country_stats["ratio"] = country.carbon_per_capita_0 / country_stats["savings"] if country_stats["savings"] > 0 else country.carbon_per_capita_0
      country_list.append(country_stats)
      country_stats = {}

    country_savings = sorted(country_list, key = lambda k : k["savings"], reverse=True)[:5]
    country_ratios = sorted(country_list, key = lambda k : k["ratio"])[:5]
    response = {
      "savings": country_savings,
      "ratios": country_ratios
    }
    
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
    

@app.route('/user', methods=['GET'])
@cross_origin()
def user():
    user_registration = request.args.get('registration')
    user = User.query.filter_by(registration=user_registration).first()
    
    sql = 'select sum(carbon_debit)-sum(carbon_credit) as points from action where user_id='+str(user.id);
    results = run_query(db, sql);
   
    points=0;
    if len(results) > 0:
        points= results[0]['points']
    else:
        points = 0
    
    if(points is None):
        points=0
    
    sql = 'select sum(id) from task where user_id='+str(user.id);
    results = run_query(db, sql);
    total_tasks=0
    if len(results) > 0:
        total_tasks= results[0]['sum(id)']
    else:
        total_tasks=0
    
    if(total_tasks is None):
        total_tasks=0
        
    sql = "select (carbon_debit-carbon_credit) as points from action where user_id ="+str(user.id)+" order by created_date desc limit 6";
    results = run_query(db, sql);
    recent_points = results
    for i in range(len(recent_points)):
        recent_points[i]=int(recent_points[i]['points']);
    
    
    response = {'total_points': int(points),'total_tasks': int(total_tasks),'recent_points':recent_points}
    return Response(json.dumps(response), mimetype='application/json')
    
  
def assign_task(user_id):
    sql = 'select id from tasks where id not in (select task_id from task where user_id='+str(user_id)+' and status="P")'; 
    results = run_query(db, sql);
    if(len(results)>0):
        randomNum = randint(0,len(results)-1)
        randomId = int(results[randomNum]['id'])
        task = Task(int(user_id), randomId, 'P')
        try:
            db.session.add(task)
            db.session.flush()
            db.session.commit()
            print "New task was assigned id "+str(randomId)
        except:
            db.session.rollback()
            print "Error creating task"

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, threaded=True)
    
