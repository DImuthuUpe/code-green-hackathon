import json

from flask import Flask, render_template, request, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import cross_origin
from sqlalchemy import text
from model import *

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://@localhost/puppy-earth'
app.debug = True

db = SQLAlchemy(app)



@app.route('/ping/<cookie>')
@cross_origin()
def ping(cookie):
    response ={}
    connection = db.engine.connect()
    sql = 'select id from user where registration = "'+cookie+'"'
    rows = connection.execute(text(sql))
    for u in rows:
        response = (dict(u))
        
    return Response(json.dumps(response),mimetype='application/json')
    
@app.route('/countries')
@cross_origin()
def index():
    countries = []
    connection = db.engine.connect()
    sql = 'select id,name from country'
    rows = connection.execute(text(sql))
    for c in rows:
        countries.append(dict(c.items()))
        
        
    return Response(json.dumps(countries), mimetype='application/json')
    

@app.route('/register',methods=['POST'])
@cross_origin()
def register():
    user_data =  json.loads( request.data )
    country_id= user_data['country_id']
    registration = user_data['registration']
    response ={}
    user = User(int(country_id),0,0,registration)
    try:
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        response={'message':'success'}
    except:
        db.session.rollback()
        response={'message':'fail'}
        
    return Response(json.dumps(response), mimetype='application/json')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081,threaded=True)