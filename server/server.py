import uuid
import json

from flask import Flask, render_template, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import cross_origin
from sqlalchemy import text

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
    sql = 'select id from user where registration = "' + cookie + '"'

    result = run_query(db, sql)
    if len(result) < 1:
      result = {}
      
    return Response(json.dumps(result), mimetype='application/json')
    
@app.route('/countries')
@cross_origin()
def countries():
    sql = 'select id, name from country'
    countries = run_query(db, sql, multi=True)

    return Response(json.dumps(countries), mimetype='application/json')

@app.route('/foods')
@cross_origin()
def foods():
    foods = []
    
    sql = 'select id, name, image from food where carbon_kilos <= 10 order by rand() limit 1'
    foods.append(run_query(db, sql, multi=True))

    sql = 'select id, name, image from food where carbon_kilos > 10 and carbon_kilos <=20 order by rand() limit 2'
    foods.append(run_query(db, sql, multi=True))

    sql = 'select id, name, image from food where carbon_kilos > 20 order by rand() limit 1'
    foods.append(run_query(db, sql, multi=True))

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
