#Version1.1 = user friendly, edit thte texts that appear

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title = "Weather API", version = "1.0")

#1.pydantic model

class WeatherResponse(BaseModel):
        city: str
        temperature: float
        humidity: float
        description: str

#2.API key + Base Url

API_KEY = "98d95dfdf6d6b91e1b9d6e4528496874"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


#3.route: get weather by city
#response model
@app.get("/{city}", response_model= WeatherResponse)
def get_weather(city:str):
    params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
    }
    response = requests.get(BASE_URL, params = params)

    if response.status_code != 200:
        raise HTTPException(status_code = 404, detail = "City not found")

    data = response.json()

    weather = WeatherResponse(
        city = data["name"],
        temperature= data["main"]["temp"],
        humidity = data["main"]["humidity"],
        description=data["weather"][0]["description"],
    )
    return weather

#4. Root route

@app.get("/hi")
def home():
     return {"message":  "Hello! I am Abror Mahir! "
     "Welcome to my Weather API (Version 1.0)"}