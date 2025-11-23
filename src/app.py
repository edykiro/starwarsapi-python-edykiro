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
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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

# User endpoints

@app.route('/users', methods=["POST"])
def crear_usuario():
    data = request.get_json()
    user = User(
        email = data.get('email'),
        username = data.get('username')
    )
    db.session.add(user)
    db.session.commit()
    return user.serialize(), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    data = db.session.execute(select(User)).scalars()

    result = list(map(lambda item: item.serialize(), data))
    print(result[0])
    
    response_body = {"results": result}
    return jsonify(response_body), 200

@app.route('/users/<int:user_id>', methods=['GET'])  
def get_single_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"Message":"User_id not found in database"})
    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])  
def delete_single_user(user_id):
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({"Message":"User_id not found in database"})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify("deleted user", user_id)

# Planet endpoints

@app.route('/planets', methods=["POST"])
def create_planet():
    data = request.get_json()
    planet = Planet(
        name = data.get('name'),
        mass = data.get('mass'),
        description = data.get('description')
    )
    db.session.add(planet)
    db.session.commit()
    return planet.serialize(), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    data = db.session.execute(select(Planet)).scalars()
    result = list(map(lambda item: item.serialize(), data))
    response_body = {"results": result}
    print("hello")
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])  
def get_single_planet(planet_id):
    planet = db.session.get(Planet, planet_id)
    return jsonify(planet.serialize()), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])  
def delete_single_planet(planet_id):
    planet = db.session.get(Planet, planet_id)
        
    if not planet:
        return jsonify({"Message":"Planet_id not found in database"})
    
    db.session.delete(planet)
    db.session.commit()
    return jsonify("deleted planet", planet_id)
    
# Starship endpoints

@app.route('/starships', methods=["POST"])
def create_starship():
    data = request.get_json()
    starship = Starship(
        name = data.get('name'),
        speed = data.get('speed'),
        faction = data.get('faction')    
    )
    db.session.add(starship)
    db.session.commit()
    return starship.serialize(), 200

@app.route('/starships', methods=['GET'])
def get_all_starships():
    data = db.session.execute(select(Starship)).scalars()
    result = list(map(lambda item: item.serialize(), data))
    response_body = {"results": result}
    print("hello")
    return jsonify(response_body), 200
    
@app.route('/starships/<int:starship_id>', methods=['GET'])  
def get_single_starship(starship_id):
    single_starship = db.session.get(Starship, starship_id)
    return jsonify(single_starship.serialize()), 200

@app.route('/starships/<int:starship_id>', methods=['DELETE'])  
def delete_single_starship(starship_id):
    starship = db.session.get(Starship, starship_id)
        
    if not starship:
        return jsonify({"Message":"Starship_id not found in database"})
    
    db.session.delete(starship)
    db.session.commit()
    return jsonify("deleted starship", starship_id)

# Character endpoints

@app.route('/characters', methods=["POST"])
def create_character():
    data = request.get_json()
    character = Character(
        name = data.get('name'),
        description = data.get('description')  
    )
    db.session.add(character)
    db.session.commit()
    return character.serialize(), 200

@app.route('/characters', methods=['GET'])
def get_all_characters():
    data = db.session.execute(select(Character)).scalars()
    result = list(map(lambda item: item.serialize(), data))
    response_body = {"results": result}
    print("hello")
    return jsonify(response_body), 200
    
@app.route('/characters/<int:character_id>', methods=['GET'])  
def get_single_character(character_id):
    single_character = db.session.get(Character, character_id)
    
    if not single_character:
        return jsonify({"message":"No character found with specified ID"})
    
    return jsonify(single_character.serialize()), 200

@app.route('/characters/<int:character_id>', methods=['DELETE'])
def del_single_character(character_id):
    single_character = db.session.get(Character, character_id)
    
    if not single_character:
        return jsonify({"Message":"No character found with specified ID"})
    
    db.session.delete(single_character)
    db.session.commit()
    return jsonify("deleted character",character_id)
    
    

# Favorites table and endpoints

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    print(user_id)
    favorites_table= db.session.get(Favorite, user_id)
    print(favorites_table.serialize())
    return jsonify(favorites_table.serialize()), 200


@app.route('/users/favorites/<int:user_id>/<string:item_type>/<int:item_id>', methods=['POST'])
def add_user_favorites(user_id,item_type,item_id):
    user=db.session.get(User, user_id)
    
    if not user:
        return ({"Message":"No user found with specified ID"}), 400
    
    favorite = db.session.execute(select(Favorite).where(Favorite.user_id == user_id)).scalars().one_or_none()
    print(favorite)
    if not favorite:
        favorite = Favorite(user_id=user_id)
        db.session.add(favorite)
        db.session.commit()
        
    if item_type == "planet":
        planet = db.session.get(Planet, item_id)
        
        if not planet:
            return jsonify({"message":"No planet found with item_id"})
        favorite.planets.append(planet)
        
    if item_type == "character":
        character = db.session.get(Character, item_id)
        
        if not character:
            return jsonify({"message":"No character found with item_id"})
        favorite.characters.append(character)

    if item_type == "starship":
        starship = db.session.get(Starship, item_id)
        
        if not starship:
            return jsonify({"message":"No starship found with item_id"})
        favorite.starships.append(starship)
    
    db.session.commit()
    
    return favorite.serialize()


@app.route('/users/favorites/<int:user_id>/<string:item_type>/<int:item_id>', methods=['DELETE'])
def delete_user_favorites(user_id,item_type,item_id):
    user=db.session.get(User, user_id)
    
    if not user:
        return ({"Message":"No user found with specified ID"}), 400
    
    favorite = db.session.execute(select(Favorite).where(Favorite.user_id == user_id)).scalars().one_or_none()
    print(favorite)
    if not favorite:
        favorite = Favorite(user_id=user_id)
        db.session.add(favorite)
        db.session.commit()
        
    if item_type == "planet":
        planet = db.session.get(Planet, item_id)
        
        if not planet:
            return jsonify({"message":"No planet found with item_id"})
        favorite.planets.remove(planet)
        
    if item_type == "character":
        character = db.session.get(Character, item_id)
        
        if not character:
            return jsonify({"message":"No character found with item_id"})
        favorite.characters.remove(character)

    if item_type == "starship":
        starship = db.session.get(Starship, item_id)
        
        if not starship:
            return jsonify({"message":"No starship found with item_id"})
        favorite.starships.remove(starship)
    
    db.session.commit()
    
    return favorite.serialize()


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
