from flask import Flask, request, redirect, url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email, Length
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SECRET_KEY'] = '*hbiubc8uyew83uq87wg8q8wq8g8gwiug8'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class Student(db.Model):
    stud_id = db.Column(db.Integer, primary_key = True)
    stud_name = db.Column(db.String(20))
    stud_age = db.Column(db.Integer)


class StudentRegisterForm(FlaskForm):
    student_name = StringField('Name: ', validators= [InputRequired(), Length(min=5, max=20)])   
    student_age = IntegerField('Age: ', validators=[InputRequired()]) 
    email = StringField('Email', validators = [InputRequired(),Email(), Length(min=10, max=30)])

class Person(db.Model):
    pers_id = db.Column(db.Integer, primary_key = True)
    pers_name = db.Column(db.String(20))
    pers_address = db.Column(db.String(40))
    pers_age = db.Column(db.Integer)
 
with app.app_context():
    db.create_all()



@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentRegisterForm()
    return render_template('index.html', form=form)



@app.route('/about')
def aboutme():
    return 'About my life'

if __name__ == '__main__':
    app.run(debug=True)