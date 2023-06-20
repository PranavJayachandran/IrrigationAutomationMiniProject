let latitude = "", longitude = "";
navigator.geolocation.getCurrentPosition(Success);

function SubmitForm() {
    let soiltype = document.getElementById("soiltype").value
    let croptype = document.getElementById("croptype").value
    let region = document.getElementById("region").value
    let temperature = document.getElementById("temperature").value
    var element = document.getElementsByClassName("loader")[0]
    element.classList.remove("hide_loader")
    GetWeatherCondition().then(result => {
        let weather = result['weather'][0]
        let weather_condition = MapWeatherToWeatherCondition(weather);
        PredictWaterRequirment(soiltype, croptype, region, temperature, weather_condition).then(result => result.text())
            .then(temp => {
                document.getElementsByClassName("prediction")[0].innerText = "Water Requirement is " + temp + " mm"
                element.classList.add("hide_loader")
            })
    });
}

function Success(position) {
    latitude = position.coords.latitude;
    longitude = position.coords.longitude;
}

function GetWeatherCondition() {
    return new Promise((resolve, reject) => {
        try {
            fetch("/getweather", {
                method: 'post',
                body: JSON.stringify({
                    latitude: latitude,
                    longitude: longitude
                }),
            }).then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    return response.json().then(error => {
                        console.log(error)
                        // Instead of throwing an error, you can handle it here
                        throw new Error(error.message);
                    });
                }
            }).then(weather => {
                resolve(weather)
            })
        }
        catch (err) {
            reject(err)
        }
    })
}

function MapWeatherToWeatherCondition(weather) {
    let weather_id = weather['id']
    if (weather_id >= 200 && weather_id <= 232)
        return 3
    else if (weather_id >= 300 && weather_id <= 321)
        return 4
    else if (weather_id >= 500 && weather_id <= 531)
        return 4
    else if (weather_id == 800)
        return 2
    else (weather_id >= 801 && weather_id <= 804)
    return 4
}

function PredictWaterRequirment(soiltype, croptype, region, temperature, weather_condition) {
    return new Promise((resolve, reject) => {
        fetch("/predict", {
            method: 'post',
            body: JSON.stringify({
                soiltype: soiltype,
                croptype: croptype,
                region: region,
                temperature: temperature,
                weather_condition: weather_condition
            }),
        }).then(response => {
            if (response.ok) {
                resolve(response);
            } else {
                reject();
            }
        })
    })
}