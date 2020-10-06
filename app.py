# this is a test file 
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# install using,  pip3 install sqlalchemy flask-sqlalchemy 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import PrimaryKeyConstraint

# this is the database connection string or link 
# brokenlaptops.db is the name of database and it will be created inside 
# project directory. You can choose any other direcoty to keep it, 
# in that case the string will look different. 
database = "sqlite:///courselist.db"


app = Flask(__name__)

# important configuration parameter, don't miss it 
app.config["SQLALCHEMY_DATABASE_URI"] = database

# database instance. this db will be used in this project 
db = SQLAlchemy(app)

@app.route('/')
def homepage():
    return render_template('homepage.html')



class BrokenLaptop(db.Model):
    department = db.Column(db.String(4), primary_key = True)
    title = db.Column(db.String(40), nullable = False)
    number = db.Column(db.Integer, nullable = False)
    section = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(400), nullable = True)
    
if __name__ == '__main__':
    app.run(debug=True)    
    