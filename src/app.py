"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planetas
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

##end points 

@app.route('/user', methods=['GET'])
def handle_hello():
    
##querys o consultas
    users_query = User.query.all()
    
    results = list(map(lambda item: item.serialize(),users_query))


    response_body = {
        "msg": "ok",
        "results": results
    }
    return jsonify(response_body), 200

# obtiene los datos de un usuario
@app.route('/user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    user = User.query.filter_by(id=user_id).first()

#  ##querys o consultas


    response_body = {
        "msg": "okk",
        "result": user.serialize()
    }

    return jsonify(response_body), 200

@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.json
    print(request_body["email"])
    

    #user_query = User.query.filter_by(email=request_body["email"]).first()

    # if user_query is None:
    user = User(email=request_body["email"], password=request_body["password"])
    db.session.add(user)
    db.session.commit()

    response_body = {
            "msg": "el susuario ",
            #"result": user_query.serialize()
        }

    return jsonify(response_body), 200
    # else:
    #     return jsonify({"msg":"Usuario ya existe"}), 400

#personajes

@app.route('/personaje', methods=['GET'])
def hola_hola():
    
##querys o consultas
    personajes_query = Personaje.query.all()
    
    results = list(map(lambda item: item.serialize(),personajes_query))


    response_body = {
        "msg": "okok",
        "results": results
    }
    return jsonify(response_body), 200

#obtiene los datos de un usuario
@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def get_info_personaje(personaje_id):
    personaje = Personaje.query.filter_by(id=personaje_id).first()

#  ##querys o consultas
  

    response_body = {
        "msg": "okk",
        "result": personaje.serialize()
    }

    return jsonify(response_body), 200

@app.route('/personaje', methods=['POST'])
def create_personaje():
    request_body = request.json
    print(request_body["nombre"])
    

    #user_query = User.query.filter_by(email=request_body["email"]).first()

    # if user_query is None:
    personaje = Personaje(nombre=request_body["nombre"], altura=request_body["altura"], genero=request_body["genero"], peso=request_body["peso"])
    db.session.add(personaje)
    db.session.commit()

    response_body = {
            "msg": "el personaje",
            #"result": user_query.serialize()
        }

    return jsonify(response_body), 200
    # else:
    #     return jsonify({"msg":"Usuario ya existe"}), 400

#planetas

@app.route('/planetas', methods=['GET'])
def mundo_mundo():
    
##querys o consultas
    planetas_query = Planetas.query.all()
    
    results = list(map(lambda item: item.serialize(),planetas_query))


    response_body = {
        "msg": "ok",
        "results": results
    }
    return jsonify(response_body), 200

#obtiene los datos de un usuario
@app.route('/planetas/<int:planetas_id>', methods=['GET'])
def get_info_planetas(planetas_id):
    planetas = Planetas.query.filter_by(id=planetas_id).first()

#  ##querys o consultas
  

    response_body = {
        "msg": "okk",
        "result": planetas.serialize()
    }

    return jsonify(response_body), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
