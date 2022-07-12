from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

# connect to sql db on heroku
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


# """ .replace("://", "ql://", 1) """
# set up car model


class URLModel(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String())
    short_id = db.Column(db.String())

    def __init__(self, url, short_id):
        self.url = url
        self.short_id = short_id

    def __repr__(self):
        return f"<URL:  {self.url}>"


@app.route('/', methods=['POST', 'GET'])
def handle_home():
    return 'Hello'


@app.route('/shorten', methods=['POST', 'GET'])
def handle_urls():
    if request.method == 'POST':

        new_url = URLModel(
            url=request.form['url'], short_id='???')
        db.session.add(new_url)
        db.session.commit()
        return {"message": f"url: {new_url.url} has been created successfully, your id is {new_url.short_id}"}

    """ elif request.method == 'GET':
        cars = URLModel.query.all()
        results = [
            {
                "id": car.id,
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]
        return {"count": len(results), "cars": results} """


@app.route('/cars/<id>', methods=['GET', 'DELETE', 'PATCH'])
def get_single_car(id):
    if request.method == 'GET':
        car = URLModel.query.get(id)
        results = {
            "id": car.id,
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        }
        return results

    elif request.method == 'DELETE':
        URLModel.query.filter_by(id=id).delete()
        db.session.commit()

        return {"message": f"car has been deleted successfully."}

    elif request.method == 'PATCH':
        data = request.get_json()
        db.session.query(URLModel).filter(
            URLModel.id == id).update({'model': data['model']})
        db.session.commit()

        return {"message": f"car has  been updated successfully."}
