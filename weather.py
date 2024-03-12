# Module imports
from time import sleep
import python_weather
import asyncio
import os
import sqlite3

current_directory = os.path.dirname(os.path.abspath(__file__))
sql_name = "carDB.sqlite3"
file_path = os.path.join(current_directory, sql_name)
db = sqlite3.connect(file_path)
cursor = db.cursor()

def units():
    print("Do you want the program to run in Imperial or Metric")
    sleep(1)
    user_input = input("Enter 'Y' for metric otherwise assumed to be imperial")
    if user_input.lower() == "y":
        unit = "METRIC"
        cursor.execute('''INSERT INTO location(units) VALUES (?)''', (unit.upper(),))
        db.commit()
        return
    else:
        unit = "IMPERIAL"
        cursor.execute('''INSERT INTO location(units) VALUES (?)''', (unit.upper(),))
        db.commit()
        return
    
def citycheck(city):
    if city == 0:
        print("We have no data saved for this program")
        sleep(2)
        print("We use a weather API in this program.")
        sleep(2)
        citysave = input("If you would like to set you location, you may now, otherwise it will automaticaly be set to Dallas TX.\n(This can be changed later)\n")
        if citysave == "Placeholder":
            citysave = "dallas"
            cursor.execute('''INSERT INTO location(location) VALUES (?)''', (citysave.capitalize(),))
            db.commit()
            return
        else: 
            cursor.execute('''INSERT INTO location(location) VALUES (?)''', (citysave.capitalize(),))
            db.commit()
            return
    else:
        cursor.execute("DELETE FROM location")
        citysave = input("You may now set your location in the program\nIf you enter nothing, it will be set to Dallas TX\n(This can be changed at any time)\n")
        if citysave == "":
            citysave = "Dallas"
            cursor.execute('''INSERT INTO location(location) VALUES (?)''', (citysave.capitalize(),))
            db.commit()
            return
        else: 
            cursor.execute('''INSERT INTO location(location) VALUES (?)''', (citysave.capitalize(),))
            db.commit()
            return
   


async def getweather(city, ifstr: bool = False):
    units = cursor.execute("SELECT units FROM location").fetchone()[0]
    if units == "METRIC":
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            weather = await client.get(city)
    else:
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            weather = await client.get(city)
    
    if ifstr == True:
        return str(weather.current.temperature)
    else:
        return weather.current.temperature
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  

  
