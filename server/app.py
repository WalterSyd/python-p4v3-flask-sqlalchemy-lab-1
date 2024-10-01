# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    if not earthquake:
        #create a dictionary response_data with a message indicating that the earthquake was not found,
        response_data = {'message': f'Earthquake {id} not found.'}
        return jsonify(response_data), 404
    #if the earthquake is found, convert it to a dictionary and return it with the status code
    response_data = earthquake.to_dict()
    return jsonify(response_data), 200


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    response_data = {'count': len(earthquakes), 'quakes': [e.to_dict() for e in earthquakes]}
    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
