from flask import Flask, request, redirect, url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email, Length
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SECRET_KEY'] = '*hbiubc8uyew83uq87wg8q8wq8g8gwiug8'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Login

login_manager = LoginManager(app)
login_manager.login_view='login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(20), unique = True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)

class UserForm(FlaskForm):
    user_name = StringField('User Name', validators=(InputRequired(), Length(min=6, max=20)))
    password = PasswordField('Password', validators=(InputRequired(), Length(min=8, max=20)))

class LoginForm(FlaskForm):
    user_name = StringField('User Name', validators=(InputRequired(), Length(min=6, max=20)))
    password = PasswordField('Password', validators=(InputRequired(), Length(min=8, max=20)))



class Student(db.Model):
    stud_id = db.Column(db.Integer, primary_key = True)
    stud_name = db.Column(db.String(20))
    stud_age = db.Column(db.Integer)


class StudentRegisterForm(FlaskForm):
    student_name = StringField('Name: ', validators= [InputRequired(), Length(min=5, max=20)])   
    student_age = IntegerField('Age: ', validators=[InputRequired()]) 
    # email = StringField('Email', validators = [InputRequired(),Email(), Length(min=10, max=30)])

class Person(db.Model):
    pers_id = db.Column(db.Integer, primary_key = True)
    pers_name = db.Column(db.String(20))
    pers_address = db.Column(db.String(40))
    pers_age = db.Column(db.Integer)
 
with app.app_context():
    db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Signup Form Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()
    return render_template('signup.html', form=form)


# Login Form Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():

    return render_template('dash.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentRegisterForm()
    details = Student.query.all()

    if form.validate_on_submit():
        lname = form.student_name.data
        myage = form.student_age.data
        try:
            person = Student(stud_name=lname, stud_age=myage)
            db.session.add(person)
            db.session.commit()
            return redirect('/')
        
        except:
            print('Data not inserted')

    return render_template('index.html', form=form, details=details)



@app.route('/about')
def aboutme():
    return 'About my life'

if __name__ == '__main__':
    app.run(debug=True)