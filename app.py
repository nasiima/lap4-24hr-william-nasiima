from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug import exceptions
import string
import random
import os

# connect to sql db on heroku
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:willwill@localhost/url_shortener'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


# """ """
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


@app.route('/', methods=['GET', 'POST'])
def url_handler():
    if request.method == 'POST':
        url = request.form['url']

        if not url:
            return render_template('index.html',text='You need to enter a URL!'), 200

       
        short_id = create_short_id(6)

        new_url = URLModel(
            url=url, short_id=short_id)
        db.session.add(new_url)
        db.session.commit()
        

        return render_template('index.html', text=f'Here is your new URL: {request.host_url + short_id}')
         
    return render_template('index.html')

# id route
@app.route('/<short_id>')
def redirect_url(short_id):
    link = URLModel.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.url)
    else:
        return render_template('index.html', text=f"That link doesn't exist, please create one here")

# short id generator        
def create_short_id(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# error handler
@app.errorhandler(404)
def handle_404(err):
    return render_template('errors/404.html'), 404

@app.errorhandler(405)
def handle_405(err):
    return render_template('errors/405.html'), 405


@app.errorhandler(500)
def handle_500(err):
    return render_template('errors/500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
