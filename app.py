from flask import Flask, jsonify, request, render_template, redirect
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


@app.route('/', methods=['GET', 'POST'])
def url_handler():
    if request.method == 'POST':
        url = request.form['url']

        if not url:
            return render_template('index.html',text='You need to enter a URL!'), 200

       
        short_id = create_short_id(6)

        new_url = URLModel(
            original_url=url, short_id=short_id)
        db.session.add(new_url)
        db.session.commit()
        

        return render_template('index.html', text=f'Here is your new URL: {request.host_url + short_id}')
         
    return render_template('index.html')

# id route
@app.route('/<short_id>')
def redirect_url(short_id):
    link = URLModel.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.original_url)
    else:
        flash('That URL is not valid!')
        return redirect(url_for('index'))

# short id generator        
def generate_short_id(num_of_chars):
    return ''.join(choice(string.ascii_lowercase+string.ascii_uppercase+string.digits) for _ in range(num_of_chars))


# error handler
@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return render_template('errors/500.html')

if __name__ == "__main__":
    app.run(debug=True)
