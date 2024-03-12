# Module used across code to gain info about client operating system
import os
# Module used for forcefully ending the program
import sys
# Module used across the code for dramatic effect
from time import sleep
# SQL module
import sqlite3
# Module used to make SQl tables prettier
from prettytable import PrettyTable
# Colors! because who dosen't like colors
from termcolor import colored
from colorama import just_fix_windows_console
# Import from support file "Car.py"
from Car import Car
# Bandaid solution for some QOL things :)
from QOL import *
# Data Scraper for SQL table add() function
from urllib.request import urlopen
from bs4 import BeautifulSoup
# Regex
import re
# Weather API??
import python_weather
import asyncio
from weather import *


while True:
    try: # Kinda want to keep this here because this info could relate farther down the program
        cursor.execute("SELECT location FROM location")
        result = cursor.fetchone()  # Assuming you expect only one row
        if result:
            city = str(result[0])
        measurement = cursor.execute("SELECT units FROM location")
        break
    except:
        cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='location' ''')
        if cursor.fetchone()[0] != 1:
            cursor.execute('''CREATE TABLE location(location TEXT PRIMARY KEY, units TEXT)''')
            units()
            city = "Placeholder"
            citycheck(city)

def intro(city):
    
    clear()

    # Number of cars in the database
    cursor.execute("SELECT COUNT (*) FROM cars")
    rowcount = cursor.fetchone()[0]
    if rowcount in (0,""):
        print("There are no cars in the database")
    elif rowcount == 1:
        print("There is 1 car in the database.")
    else:
        print("There is ", rowcount, " cars in the database.")
    
    # Main menu frontend
    checkcars("1. Pick a car to continue", rowcount) 
    print("2. Add a car")
    checkcars("3. Remove a car", rowcount)
    checkcars("4. Update a car", rowcount)
    checkcars("5. Show all cars", rowcount)
    print("6. Update weather location")
    print("7. Exit")
    
    # Processing of the input
    if rowcount in (0,""):
        part1 = "You can't choose any options that are "
        part2 = colored("red", "red", attrs=["bold"])
        print(part1 + part2)
    userInput = get_numeric_input("What do you choose? Enter a number\n", intro, True)
    choice = int(userInput)
    # This needs to be checked first
    if choice in (1,3,4,5) and rowcount in (0,""):
        intro(city)
    elif choice == 31218:
        cursor.execute('''DROP TABLE cars''') # A little lazy to make a for loop
        cursor.execute('''DROP TABLE location''') # I might do it later if I get more tables (should I just use a json?)
        input("Deleted all the table\nReturning back to the main menu\n")
    else:
        options = {
        1 : showOne,
        2 : add,
        3 : remove,
        4 : update,
        5 : showAll,
        6 : citycheck
        }
        for numchoice, function in options.items():
            if choice == 6:
                citycheck(city)
                intro(city)
            elif choice == numchoice:
                function()
                break
        else:
            if choice == 7:
                clear()
                print("Saving cars and exiting program")
                sys.exit()
            else:
                print("This is not an option")
                input("Press enter to continue")
                intro(city)


def showAll():
    clear()
    cur = cursor.execute("SELECT * from cars")
    t = PrettyTable(["ID", "Brand", "Price [usd.]", "Year", "Car Type", "Is car leased?"])
    for row in cur:
        row = list(row)
        if row[5]:
            leasing = "Yes"
        else:
            leasing = "No"
        numericformat(row[2], row, 2)
        t.add_row([row[0], row[1], "$" + str(row[2]), row[3], row[4], leasing])
    print(t)
    input("Press enter to continue")
    intro(city)


def add():
    clear()
    print('What is the brand of the car? Write "a" to cancel\n')
    print('Or write "i" to import a car from bilhandel.dk\n')
    brandInput = input(colored("The website import doesn't work for now\n", "red", attrs=["bold", "underline"]))
    if brandInput.lower() == "a":
        intro(city)
    elif brandInput.lower() == "i":
        clear()
        url = input("Enter URL for the car you want to import\n")
        try:
            page = urlopen(url)
        except:
            print("Error opening the URL")
        else:
            clear()
            soup = BeautifulSoup(page, 'html.parser')

            contentTitle = soup.find('div', {"class": "col-xs-8"})
            title = ''

            for x in contentTitle.findAll('h1'):
                title = title + ' ' + x.text
                if len(title) > 0:
                    titleSplit = title.split()
                    title = titleSplit[0]

                contentPrice = soup.find('div', {"class": "col-xs-4"})
                price = ''
                for x in contentPrice.findAll('div'):
                    price = price + ' ' + x.text

                contentYear = soup.find('div', {"style": "font-size: 16px;padding-left:15px;"})
                year = ''
                for x in contentYear.findAll('span'):
                    year = year + ' ' + x.text

                priceOutput = re.sub('\D', '', price)
                yearSplit = year.split()
                if len(yearSplit) > 0:
                    yearOutput = re.sub('\D', '', yearSplit[4])

                cartypeInput = input("What type of car is it?\n")
                isLeasingCarInput = input("Is the car leased?\n").lower()
                if isLeasingCarInput in yeslist:
                    cursor.execute(
                        ''' INSERT INTO cars(brand, price, year, cartype, isLeasingCar) VALUES (?,?,?,?,?) ''',
                        (title, priceOutput, yearOutput, cartypeInput, 1))
                else:
                    cursor.execute(
                        ''' INSERT INTO cars(brand, price, year, cartype, isLeasingCar) VALUES (?,?,?,?,?) ''',
                        (title, priceOutput, yearOutput, cartypeInput, 0))
                db.commit()
                intro(city)
    else:
        priceInput = get_numeric_input('What is the price of the car?\n')
        yearInput = get_numeric_input("What year is the car from?\n")
        cartypeInput = input("What type of car is it?\n")
        isLeasingCarInput = input("Is the car leased?\n").lower()
        if isLeasingCarInput in yeslist:
            cursor.execute(''' INSERT INTO cars(brand, price, year, cartype, isLeasingCar) VALUES (?,?,?,?,?) ''',
                           (brandInput.capitalize(), priceInput, yearInput, cartypeInput, 1))
        else:
            cursor.execute(''' INSERT INTO cars(brand, price, year, cartype, isLeasingCar) VALUES (?,?,?,?,?) ''',
                           (brandInput.capitalize(), priceInput, yearInput, cartypeInput, 0))
        db.commit()
        intro(city)


def remove():
    clear()
    cur = cursor.execute("SELECT id, brand, price, year, cartype, isLeasingCar from cars")
    t = PrettyTable(["ID", "Brand", "Price [usd.]", "Year", "Car Type", "Is car leased?"])
    for row in cur:
        row = list(row)
        if row[5]:
            leasing = "Yes"
        else:
            leasing = "No"
        numericformat(row[2], row, 2)
        t.add_row([row[0], row[1], "$" + str(row[2]), row[3], row[4], leasing])
    print(t)
    print('What car do you want to remove? Enter ID')
    carID = input('Write "a" to cancel\n')
    if carID.lower() == "a":
        intro(city)
    elif carID.lower() == "clr":
        sqlDelete = '''DELETE from cars where id=*'''
        cursor.execute(sqlDelete)
        db.commit()
        print("Everything has been wiped")
        intro(city)
    else:
        if input("This is a permanent decison\nWrite 'a' if you want to go back to the beginning(You will be soft locked to delete a car)\n") == 'a':
            intro(city)
        else: get_numeric_input(carID, remove)
        sqlDelete = '''DELETE from cars where id=?'''
        sqlData = (int(carID))
        cursor.execute(sqlDelete, (int(sqlData),))
        db.commit()
        intro(city)

def update():
    clear()
    cur = cursor.execute("SELECT id, brand, price, year, cartype, isLeasingCar from cars")
    t = PrettyTable(["ID", "Brand", "Price [usd.]", "Year", "Car Type", "Is car leased?"])
    for row in cur:
        row = list(row)
        if row[5]:
            leasing = "Yes"
        else:
            leasing = "No"
        numericformat(row[2], row, 2)
        t.add_row([row[0], row[1], "$" + str(row[2]), row[3], row[4], leasing])
    print(t)
    
    while True:
        sqlUpdate = '''SELECT * FROM cars WHERE id = ?'''
        carID = input('What car do you want to update? Enter ID\nWrite "a" to cancel\n')
        if carID.lower() == "a":
            intro(city)
        else:
            attempts = 0
            try:
                int(carID)
            except ValueError:
                attempts += 1
                print("Please enter a valid numerical value.")
                if attempts < 2:
                    sleep(1)
                    update()
                if attempts >= 2:
                    print("Try removing any special characters like commas")
                    sleep(1)
                    update()
            
            cur = cursor.execute(sqlUpdate, (int(carID),))
            clear()
            for row in cur:
                print("1. Brand:", row[1].capitalize())
                print("2. Price:", "$" + str(row[2]))
                print("3. Year:", row[3])
                print("4. Car Type:", row[4].capitalize())
                if row[5] == 0:
                    print("5. Leasing status: The car is not leased")
                else:
                    print("5. Leasing status: The car is leased")
                print("6. Exit")

            userInput = get_numeric_input("What do you want to update? Enter number\n")
            if userInput == 6:
                clear()
                intro(city)
            elif userInput in range(1, 6):
                update_car_detail(userInput, carID)

def update_car_detail(choice, carID):
    clear()
    if choice == 1:
        up = 'brand'
        new = input("What is the new brand for the car?\n")
    elif choice == 2:
        up = 'price'
        new = get_numeric_input("What is the new price for the car?\n")
    elif choice == 3:
        up = 'year'
        new = get_numeric_input("What is the new year for the car?\n")
    elif choice == 4:
        up = 'cartype'
        new = input("What is the updated car type?\n")
    elif choice == 5:
        up = 'isLeasingCar'
        leasing_input = input("Is the car leased? (Yes/No)\n").lower()
        new = 1 if leasing_input == 'yes' else 0

    sqlUpdate = '''UPDATE cars SET '''+up+''' = ? WHERE id = ?'''
    cursor.execute(sqlUpdate, (new, carID))
    db.commit()
    update()

def showOne():
    clear()
    print("Do you want to search by Brand or ID\nPress 'b' for brand or 'i' for ID")
    searchtype = input("Note: it is recommended to use Brand search first in case if you have multiple cars of the same brand\n")
    if searchtype == "b":
        sqlSearch = ''' SELECT * from cars WHERE brand =?'''
        sqlData = (input("Search for car brand: "))
        cur = cursor.execute(sqlSearch, (sqlData.capitalize(),))
        if cur.fetchone():
            clear()
            cur = cursor.execute(sqlSearch, (sqlData.capitalize(),))
            t = PrettyTable(["ID", "Brand", "Price [usd.]", "Year", "Car Type", "Is car leased?"])
            print("Showing results for", sqlData)
            for row in cur:
                row = list(row)
                if row[5]:
                    leasing = "Yes"
                else:
                    leasing = "No"
            numericformat(row[2], row, 2)
            t.add_row([row[0], row[1], "$" + str(row[2]), row[3], row[4], leasing])
            print(t)
            carpick = input("Is this car correct?\n")
            if carpick in yeslist:
                currentcar = str((cursor.execute(''' SELECT price from cars WHERE ID = ?''', (sqlData,)).fetchone()))
                removalpattern = r'[(),]'
                currentcar = re.sub(removalpattern, '', currentcar)
            else:
                caryes = input("Sorry about that\nWould you like to try again press 'a' or restart? press 'r'")
                try:
                    if caryes == "a":
                        showOne()
                except:
                    print("That value isn't accepted")
                else:
                    if caryes == "r":
                        intro(city)
        else:
            clear()
            print("There was no results for the brand", sqlData + ".")
            userInput = input("Do you want to add a new car?\n").lower()
            print(userInput)
            if userInput in yeslist:
                add()
            else:
                intro(city)
        intro(city)
    elif searchtype == "i":
        sqlSearch = ''' SELECT * from cars WHERE ID =?'''
        sqlData = (input("Search for car ID: "))
        cur = cursor.execute(sqlSearch, (sqlData.capitalize(),))
        if cur.fetchone():
            clear()
            cur = cursor.execute(sqlSearch, (sqlData.capitalize(),))
            t = PrettyTable(["ID", "Brand", "Price [usd.]", "Year", "Car Type", "Is car leased?"])
            print("Showing results for", sqlData)
            for row in cur:
                row = list(row)
                if row[5]:
                    leasing = "Yes"
                else:
                    leasing = "No"
            numericformat(row[2], row, 2)
            t.add_row([row[0], row[1], "$" + str(row[2]), row[3], row[4], leasing])
            print(t)
            carpick = input("Is this car correct?\n")
            if carpick in yeslist:
                cursor.execute('''DELETE FROM cache''')
                cursor.execute('''INSERT INTO cache(choosen) VALUES (?)''', (sqlData))
                currentcar = cursor.execute('''SELECT price FROM cars WHERE ID = ?''', (sqlData,)).fetchone() # This code doesn't work but it does its job of breaking out of this function
            else:
                caryes = input("Sorry about that\nWould you like to try again press 'a' or restart? press 'r'")
                try:
                    if caryes == "a":
                        showOne()
                except:
                    print("That value isn't accepted")
                else:
                    if caryes == "r":
                        intro(city)
        else:
            clear()
            print("There was no results for the ID", sqlData + ".")
            userInput = input("Do you want to add a new car?\n").lower()
            print(userInput)
            if userInput in yeslist:
                add()
            else:
                intro(city)
    else:
        print("That is not a valid input")
        clear()
        showOne()

intro(city)

db.commit()
# Can't close the database here to retrieve weather info for later
cursor.execute('''SELECT choosen FROM cache''')
results = cursor.fetchall()
choosen_values = [row[0] for row in results]

for value in choosen_values:
    currentcar_result = cursor.execute('''SELECT price FROM cars WHERE ID = ?''', (value,)).fetchone()
    if currentcar_result:
        currentcar_int = int(currentcar_result[0])  # Convert to integer
        currentcar_str = str(currentcar_int)  # Convert to string for manipulation
        currentcar_str = re.sub(r'[(),]', '', currentcar_str)  # Perform string manipulation
        currentcar_int = int(currentcar_str)  # Convert back to integer

print("Thank you for setting up you car")
sleep(2)
print("You may now calculate how long it will take for your car to reach it's destination and how far the destination is")
sleep(2)
#distance calc
#pos inputs
carpos = []
clear()
carx = get_numeric_input("What is your car's starting X position?\n")
carpos.append(carx)
clear()
cary = get_numeric_input("What is your car's starting Y position?\n")
carpos.append(cary)
clear()
des = get_numeric_input("Input your destination's X position\n")
clear()
des1 = get_numeric_input("Input your destination's Y position\n")
clear()
#Row Magic
t = PrettyTable([" ","X Position", "Y Position"])
t.add_row(["Starting Position", carx, cary])
t.add_row(["Ending Location", des, des1])
#calc
des = int(des) - int(carpos[0])
des1 = int(des1) - int(carpos[1])

# Integer Fix
des = abs(des)
des1 = abs(des1)

# Row Magic Pt.2
t.add_row(["Delta", des, des1])
des = des + des1
if measurement == "METRIC":
    print("It is", (temperature := asyncio.run(getweather(city, True))), "Celsius outside")# The 'temperature' variables are strings
else:
    print("It is", (temperature := asyncio.run(getweather(city, True))), "Fahrenheit outside")
# What happens if the distance to get somewhere is 0

if des == 0:
    print("Why did you input the same coordinates twice?")
    print("Well as a punishment you ain't gonna be using this program")
    print("Better luck next time!")
    sys.exit()
sleep(1)
print(f"Your car will have to drive {des} blocks to reach your destination!")

#block to mile
miles = des / 20
if measurement == "METRIC":
    miles = miles * 1.609
sleep(1)
print("According to the information you have given")
print(t)
if measurement == "METRIC":
    print(f"Your car will have to drive {miles} kilometers to reach your destination!")
else:
    print(f"Your car will have to drive {miles} miles to reach your destination!")

# car time calc(based on value)
# Dictionary to store value thresholds and corresponding coefficients
value_coefficients = {
    100000: 0.1,
    50000: 0.75,
    25000: 1,
    10000: 1.25,
    5000: 1.6,
    1000: 2,
}

# Find the appropriate coefficient based on car.value
int(currentcar_int) # Backup :)
for threshold, coefficient in sorted(value_coefficients.items(), reverse=True):
    if currentcar_int >= threshold:
        ime = coefficient * des
        break
else:
    ime = 5 * des

print(f"It will take {ime} minutes to arrive at your destination")
print("But with the temperature outside, it will take")  
# I need to find the values the api can return and use a dictionary to modify the time taken to reach the destination
# That could be an idea but not for now
temperature = asyncio.run(getweather(city))
db.close()
if measurement == "METRIC":
    if 19.5 <= temperature <= 20.5:
        enginedef = 0
    else:
        if temperature <= 19.5:
            enginedef = 19.5 - temperature
        else:
            enginedef = temperature - 20.5 
else:
    if 67 <= temperature <= 69:
        enginedef = 0
    else:
        if temperature <= 67:
            enginedef = 67 - temperature
        else:
            enginedef = temperature - 69
abs(enginedef)
debuff=[]
debuff = fibonacci(enginedef)
timeconv = 0.01
debufflist = list(map(lambda i : i * timeconv, debuff)) # takes the fib result and converts it to min.sec of a minute
for i in range(len(debufflist)):
    if i == 0:
        combined = debufflist[i]
    else:
        combined = combined + debufflist[i]
ime = float(ime) + float(combined)
combined = 60 * combined
print(combined, "extra seconds for you to arrive at your destination")
sleep(1)
clear()
print("In other words,")
sleep(1)
print(f"It will take {ime} minutes to arrive at your destination")          
# gas calc
speedword = 0
while True:
    sped = input("How fast do you want to go?\nFast?\nMedium?\nSlow?\n")
    spedwords = { # Needs to fix to work over different unit inputs
        'fast': 10,
        'medium': 35,
        'slow': 65,
    }
    for word, co in spedwords.items():
        if word in sped.lower():
            gas = miles / co
            speedword = co
            break
    else:
        print("Invalid speed input. Please choose from 'Fast', 'Medium', or 'Slow'.")
        continue

    print("You will use %.2f gallons" % gas)
    print(f"In other words, you will use {speedword} miles per gallon")
    break
