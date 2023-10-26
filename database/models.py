from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class WeatherData(Base):
    '''
        Model for WeatherData

        Attributes:
            id (int): The unique identifier for a weather record.
            city (str): The name of the city associated with the weather record.
            date (datetime): The date and time of the weather record, with a default value of the current date and time.
            temperature (int): The temperature recorded in the weather data.
            description (str): The weather description for the recorded data.
    '''
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(255))
    date = Column(DateTime, default=datetime.now())
    temperature = Column(Integer)
    description = Column(String(255))
