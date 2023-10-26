from fastapi import FastAPI, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from database.models import WeatherData
from database.database import SessionLocal
from datetime import datetime
from dotenv import load_dotenv
import uvicorn
import os


load_dotenv()
app = FastAPI()

# Your secret token
SECRET_TOKEN = os.getenv("SECRET_TOKEN")


# Custom middleware to check the 'x-token' header
class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Get the 'x-token' header from the request
        token = request.headers.get("x-token")

        # Check if the token is missing or doesn't match the secret token
        if token is None or token != SECRET_TOKEN:
            # Create a JSON response with an error message and a 401 status code
            response = JSONResponse(content={"error": "Invalid or missing token"}, status_code=401)
            return response
        
        # If the token is valid, continue to the next handler in the middleware chain
        response = await call_next(request)
        return response

# add middleware
app.add_middleware(TokenMiddleware)


# Define a route that accepts the 'day' parameter (default is None)
@app.get("/get-weather/")
async def get_weather_by_date(day: str = None):
    try:

        # Check if 'day' parameter is missing
        if not day:
            response = JSONResponse(content={"error": "required parameter 'day' not specified"}, status_code=400)
            return response
        
        # Try to parse 'day' as a valid date in 'Y-m-d' format
        try:
            datetime.strptime(day, "%Y-%m-%d")
        except ValueError:
            response = JSONResponse(content={"error": "Invalid 'day' format. Use 'Y-m-d' format"}, status_code=400)
            return response

        # Create a database session
        db = SessionLocal()
        weather_data = db.query(WeatherData).filter(WeatherData.date.like(f"{day}%")).all()
        db.close()

        # Check if no weather data is found for the specified date
        if not weather_data:
            response = JSONResponse(content={"error": "No weather data found for the specified date"}, status_code=404)
            return response
        
        # Prepare a list of weather data as JSON objects with specific fields
        weather_list = [
            {
                "city": item.city,
                "temperature": item.temperature,
                "description": item.description,
                "time": item.date.strftime("%H:%M")
            }
            for item in weather_data
        ]

        return weather_list
    except Exception as err:
        return {"error": str(err)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)