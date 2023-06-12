from flask import Flask,render_template,request
import os
import requests
app = Flask(__name__)
 
from flask import jsonify
from flask_jwt import JWT, jwt_required
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
 
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

@app.route('/register', methods=['POST'])
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

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/login', methods=['GET'])
def login():
    return render_template('main.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token = jwt.jwt_encode_callback({'email': email})
        return jsonify({'token': token.decode('utf-8')})

    return jsonify({'message': 'Invalid credentials'}), 401

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        return user

def identity(payload):
    email = payload['email']
    return User.query.filter_by(email=email).first()

jwt = JWT(app, authenticate, identity)


 
 
 
 
 
@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/home')
def home():
    return render_template("home.html")

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
    print(soiltype,croptype,temperature,region,weather_condition)
    return "done"
# main driver function
if __name__ == '__main__':
    app.run()