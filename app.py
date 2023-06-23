from flask import Flask,render_template,request,jsonify,redirect
import os
import requests
from flask_jwt_extended import JWTManager, jwt_required,create_access_token
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import pickle
import pandas as pd

app = Flask(__name__)

app.config['SECRET_KEY'] = 'random'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///irrigation.sqlite3'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    token = create_access_token(identity=username)
        # return jsonify({'token': token.decode('utf-8')})

    return render_template("main.html")


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity=username)
        # return jsonify({'token': token.decode('utf-8')})
        return redirect("/main")

    return jsonify({'message': 'Invalid credentials'}), 401

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        return user

def identity(payload):
    email = payload['email']
    return User.query.filter_by(email=email).first()

jwt = JWTManager(app)



 
@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/home')
def home():
    return render_template("home.html")
@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/getweather",methods=['POST'])
def getweather():
    input_json = request.get_json(force=True)
    latitude=input_json['latitude']
    longitude=input_json['longitude']
    weather_api_key=os.environ["WEATHER_API_KEY"]
    url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s"%(latitude,longitude,weather_api_key)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return(response.json())
 
@app.route("/predict",methods=["POST"])
def predictwaterrequirement():
    input_json = request.get_json(force=True)
    soiltype=input_json['soiltype']
    croptype=input_json['croptype']
    temperature=input_json['temperature']
    region=input_json['region']
    weather_condition=input_json['weather_condition']
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)

    new_data = pd.DataFrame({
    'CROP TYPE': [croptype],
    'SOIL TYPE': [soiltype],
    'REGION': [region],
    'TEMPERATURE GROUP': [3],
    'WEATHER CONDITION': [weather_condition]
    })
    prediction = model.predict(new_data)
    return str((round(prediction[0], 2)))

with app.app_context():
    db.create_all()
# main driver function
if __name__ == '__main__':
    app.run()