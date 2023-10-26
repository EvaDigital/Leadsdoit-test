from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
from datetime import datetime
import requests
from database.database import SessionLocal 
from database.models import WeatherData
import os

load_dotenv()

app = Celery("tasks", broker="redis://redis:6379/0")


def put_data_to_db(data):
    try:
        # Extract data from the input dictionary.
        city = data['city']
        temperature = data['temperature']
        description = data['description']
        
        # Create a new database session.
        db = SessionLocal()
        weather_data = WeatherData(city=city, temperature=temperature, description=description)
        db.add(weather_data)

        # Commit the changes to the database and close the session.
        db.commit()
        db.close()
      
    except Exception as err:
        return {'error': str(err)}


@app.task
def get_weather_task():
    try:
        # Get city and API key from environment variables.
        city = os.getenv("CITY")
        api_key = os.getenv("OPEN_WEATHER_API_KEY")

        # Construct the URL for the weather data API.
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the response data if the request is successful.
            weather_data = response.json()
            temperature_kelvin = weather_data["main"]["temp"]
            temperature = int(temperature_kelvin - 273.15)
            description = weather_data["weather"][0]["main"]

            # Create a data dictionary with extracted weather information and store it in the database.
            data = {
                "city": city,
                "temperature": temperature,
                "description": description
            }
            put_data_to_db(data)
            return {"Successful"}
        else:
            return {'status_code': response.status_code}
    except Exception as err:
        return {"error": str(err)}
    

# Define the time interval for the scheduled task (get-weather-task) in minutes.
interval = int(os.getenv("GET_WEATHER_MINUTS_TIME_INTERVAL", 60))

# Configure the Celery Beat schedule for the get-weather-task.
app.conf.beat_schedule = {
    "get-weather-task": {
        "task": "celery_app.celery.get_weather_task",
        "schedule": crontab(minute=f"*/{interval}"),
    }
}

# Set the timezone for the Celery Beat schedule.
app.conf.timezone = "UTC"
