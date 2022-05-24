
from psutil import users
from requests import Session
from db import ParkingSpace,User
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template, request, flash, redirect,session


app = Flask(__name__)

app.secret_key = "ajksdaksj"

def opendb():
    engine=create_engine("sqlite:///Carpark.sqlite",echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/startparking')
def about():
    return render_template('startparking.html')

@app.route('/uploadImg')
def contact_us():
    return render_template('uploadImg.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        #print(username,password)
        if username and password:
            db= opendb()
            result = db.query(User).filter_by(username=username,password=password).first()
            if result:
                session['is_auth'] = True
                session['id'] = result.id
                session['username'] = result.username
                flash('You are logged in!','success')
                return redirect('/')
            else:
                flash('invalid credentials','danger')
        else:
            flash('invalid form data','danger')    
    return render_template('login.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        cpassword = request.form.get('confirmpassword')
        if password != cpassword:
            flash('Password does not match','danger')
            return redirect('/register')
        else:
            db = opendb()
            user = User(username=username,password=password)
            db.add(user)
            db.commit()
            db.close()
            flash('User added successfully','success')
            return redirect('/register')
    return render_template('register.html')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)