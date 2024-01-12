#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get_all_plants(self):
        plants_list = [plant.to_dict() for plant in Plant.query.all()]
        response = make_response(
        jsonify(plants_list),
        200,
        )
        return response
    def post_plant(self):
        new_plant = Plant(
            name = request.form['name'],
            image = request.form['image'],
            price = request.form['price'],
        )
        db.session.add(new_plant)
        db.session.commit()

        new_plant_dict = new_plant.to_dict()
        response = make_response(
            jsonify(new_plant_dict),
            200,
        )
        response.headers['Content-Type'] = 'application/json'
    
        return response


class PlantByID(Resource):
    def get_plants_by_id(self, id):
        plant_by_id = Plant.query.filter_by(id=id).first().to_dict()
        response = make_response(
            jsonify(plant_by_id),
            200,
        )
        return response
    
    pass
        
app.add_resource(Plants, '/plants')
app.add_resource(PlantByID, '/plants/<int:id>')
if __name__ == '__main__':
    app.run(port=5555, debug=True)
