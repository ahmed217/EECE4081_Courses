# Import statements
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

# database creation
database = "sqlite:///courselist.db"
app = Flask(__name__)

# important configuration parameter, don't miss it 
app.config["SQLALCHEMY_DATABASE_URI"] = database

# database instance. this db will be used in this project 
db = SQLAlchemy(app)


# Functions---initialize database, test app
@app.route('/init_db')
def init_db():
    db.drop_all()
    db.create_all()
    return 'Database initialized'

@app.route('/test')
def test():
    return "App is running."


# Function---homepage
@app.route('/', methods = ['GET','POST'])
def homepage():
    course = Course.query.all()
    return render_template("homepage.html", course=course)

# Functions---CRUD
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

@app.route('/update/<course_id>', methods=['GET','POST']) 
def update(course_id): 
    
    course = Course.query.get(course_id)
    if request.form:
        newdepartment = request.form.get("department")
        newtitle = request.form.get("title")
        newnumber = request.form.get("number")
        newsection = request.form.get("section")
        newdescription = request.form.get("description")
        newsection = str(newsection).zfill(3)
        course.department = newdepartment
        course.title = newtitle
        course.number = newnumber
        course.section = newsection
        course.description = newdescription
        db.session.commit()
        
        return redirect('/', code = 302)
    return render_template("update.html", course = course, title = 'Update a course')

@app.route('/delete/<course_id>')
def delete(course_id):
    course = Course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
    course = Course.query.all()
    return redirect("/", code = 302)

# Course object
class Course(db.Model):
    department = db.Column(db.String(4), nullable = False)
    title = db.Column(db.String(40), nullable = False)
    number = db.Column(db.Integer, nullable = False)
    section = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(400), nullable = True)
    id = db.Column(db.Integer, primary_key=True)
    
if __name__ == '__main__':
    app.run(debug=True)