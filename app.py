from flask import Flask,render_template,url_for,redirect,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,ValidationError
from flask_bcrypt import Bcrypt
from login import Login
from register import Signin

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='unknownsecretkey'
db=SQLAlchemy(app)
lg=Login()
rg=Signin()



class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(25),nullable=False)
    email=db.Column(db.String(30),nullable=False,unique=True)
    phone=db.Column(db.String(13),nullable=False,unique=True)
    gender=db.Column(db.String(6),nullable=True)
   
with app.app_context():
    db.create_all() 


@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register',methods=['GET','POST'])
def register_post():
    name=request.form.get('name')
    email=request.form.get('email')
    phone=request.form.get('phone')
    gender=request.form.get('gender')
    
    filename=email[:email.find("@gmail.com")]
    
    user=User.query.filter_by(email=email).first() 
    if user:
        flash('Already a user!')
        return redirect(url_for('register'))
    
    new_user=User(name=name,email=email,phone=phone,gender=gender)
    db.session.add(new_user)
    db.session.commit()
    rg.registerFace(filename)
    return redirect(url_for('login'))


@app.route('/loginSuccess')
def loginSuccess():
    return render_template('login_success.html')
    

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login_post():
    email=request.form.get('email')
    filename=email[:email.find("@gmail.com")]
    
    user = User.query.filter_by(email=email).first()
    
    try:
        encodeList=lg.readEncodings(filename)
        status=True if lg.Authenticate(encodeList) else False
    except FileNotFoundError:
        flash('User Not registered')
        return redirect(url_for('register'))
    

    if not user:
        flash('User Not registered')
        return redirect(url_for('register'))
    if status:
        return redirect(url_for('loginSuccess'))   


if __name__=='__main__':
    app.run(debug=True)