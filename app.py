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

@app.route('/', methods = ['GET','POST'])
def homepage():
    course = Course.query.all() 
    return render_template("homepage.html", course=course)

# added individual routes for each course header

@app.route('/bio')
def bio():
    return render_template("bio.html")

@app.route('/civ')
def civ():
    return render_template("civ.html")

@app.route('/eece')
def eece():
    return render_template("eece.html")

@app.route('/mech')
def mech():
    return render_template("mech.html")

@app.route('/tech')
def tech():
    return render_template("tech.html")


@app.route('/init_db')
def init_db():
    db.drop_all()
    db.create_all()
    return 'Database initialized'

@app.route('/test')
def test():
    return "App is running."

   
@app.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        department = request.form.get("department")
        title = request.form.get("title")
        number = request.form.get("number")
        section = request.form.get("section")
        description = request.form.get("description")
        course = Course(department=department, title=title, number=number, section=section, description=description)
        db.session.add(course)
        db.session.commit()
        return redirect('/', code = 302)
    course = Course.query.all() 
    return render_template("create.html", course = course, title = 'Add a course')

    
    
@app.route('/delete/<course_id>')
def delete(course_id):
    course = Course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
    course = Course.query.all() 
    return redirect("/", code = 302)

@app.route('/update/<course_id>', methods=['GET','POST']) 
def update(course_id): 
    
    course = Course.query.get(course_id)
    if request.form:
        course.department = request.form.get("department")
        course.title = request.form.get("title")
        course.number = request.form.get("number")
        course.section = request.form.get("section")
        course.description = request.form.get("description")
        db.session.commit()
        
        return redirect('/', code = 302)
    return render_template("update.html", course = course, title = 'Update a course')




class Course(db.Model):
    department = db.Column(db.String(4), nullable = False)
    title = db.Column(db.String(40), nullable = False)
    number = db.Column(db.Integer, nullable = False)
    section = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(400), nullable = True)
    id = db.Column(db.Integer, primary_key=True)
    
if __name__ == '__main__':
    app.run(debug=True)    
    