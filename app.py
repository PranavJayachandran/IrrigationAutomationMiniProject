from flask import Flask,render_template,request
import os
import requests
app = Flask(__name__)
 
@app.route('/homepage')
def homepage():
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