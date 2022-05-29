
from main import start_watching
import os
import db
from psutil import users
from requests import Session
from db import ParkingSpace,User
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request, flash, redirect,session


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

@app.route('/startparkingapi')
def start_camera():
    start_watching()
    return jsonify({'status':'success'})

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

@app.route('/logout')
def logout():
    session['is_auth'] = False
    session.pop('username')
    return render_template('index.html')
    return render_template('index')

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

@app.route('/upload', methods=['GET','POST'])
def uploadImage():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            flash('No file uploaded','danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('no file selected','danger')
            return redirect(request.url)
        else:
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename ))
            upload = ParkingSpace(img =f"/static/uploads/{filename}", imgtype = os.path.splitext(file.filename)[1],user_id=users.id)
            db.session.add(upload)
            db.session.commit()
            flash('file uploaded and saved','success')
            session['uploaded_file'] = f"/static/uploads/{filename}"
            return redirect(request.url)
    return render_template('upload.html',title='upload new Image')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)