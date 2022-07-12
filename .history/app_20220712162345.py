from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

# connect to sql db on heroku
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL').replace("://", "ql://", 1)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# set up car model


class URLModel(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String())
    short_url = db.Column(db.String())

    def __init__(self, url, short_url):
        self.url = url
        self.short_url = short_url

    def __repr__(self):
        return f"<URL:  {self.url}>"

@app.route('/shorten', methods=['POST', 'GET'])
def handle_urls():
    if request.method == 'POST':
        
        new_url = URLModel(
            name=request.form['name'], model=request.form['model'], doors=request.form['doors'])
        db.session.add(new_car)
        db.session.commit()
        return {"message": f"car {new_car.name} has been created successfully."}
      

    elif request.method == 'GET':
        cars = CarsModel.query.all()
        results = [
            {
                "id": car.id,
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]
        return {"count": len(results), "cars": results}

# crud get by ids


@app.route('/cars/<id>', methods=['GET', 'DELETE', 'PATCH'])
def get_single_car(id):
    if request.method == 'GET':
        car = CarsModel.query.get(id)
        results = {
            "id": car.id,
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        }
        return results

    elif request.method == 'DELETE':
        CarsModel.query.filter_by(id=id).delete()
        db.session.commit()

        return {"message": f"car has been deleted successfully."}

    elif request.method == 'PATCH':
        data = request.get_json()
        db.session.query(CarsModel).filter(
            CarsModel.id == id).update({'model': data['model']})
        db.session.commit()

        return {"message": f"car has  been updated successfully."}
