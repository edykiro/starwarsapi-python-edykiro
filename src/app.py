"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from sqlalchemy import select
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Starship, Favorite
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





@app.route('/users', methods=['GET']) #GET es opcional
def get_all_users():
    data = db.session.execute(select(User)).scalars()
    result = list(map(lambda item: item.serialize(),data))
    response_body={"results": result}
    print("hello")
    return jsonify(response_body),200

@app.route('/planets', methods=['GET']) #GET es opcional
def get_all_planets():
    data = list(db.session.execute(select(Planet)).scalars())
    
    
    return test


@app.route('/user', methods=['GET']) #GET es opcional
def get_single_user():
    user_id = request.args.get("user_id")
    test = db.session.execute(select(User)).scalars()
    print(f"user_id es {user_id}")
    print(test)

    return "funciona"



















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
