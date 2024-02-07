# Module for data serialization of a list
import pickle
# Module used for forcefully ending the program
import sys
# Module used across the code for dramatic effect
import time
# Module to specify which path to save the file carinfo
from pathlib import Path
savepath = Path(getenv('USERPROFILE')) / "downloads"
import sqlite3
from Car import Car
import os
from prettytable import PrettyTable
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# Yes List with the Extension Plus Feature
yeslist = ["yes","y","of course","yea","okay","yeah","ok","alright","yep","ay","aye",
"positively","all right","yo","certainly","absolutely","exactly","indeed","okeydokey",
"undoubtedly","assuredly","unquestionably","indisputably","all right","alright","very well",
"of course","by all means","sure","certainly","absolutely","indeed","affirmative","in the affirmative",
"agreed","roger","aye","aye aye","yeah","yah","yep","yup","uh-huh","okay","OK","okey-dokey","okey-doke",
"achcha","righto","righty-ho","surely","yea"]

def get_numeric_input(prompt):
    attempts = 0
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid numerical value.")
            attempts += 1
            if attempts >= 2:
                print("Try removing any special characters like commas")
                
def caps(prompt):
    prompt = input(prompt)
    prompt = prompt.title()
    return prompt

def savetolist(prompt):
    carinfo.append(prompt.name)
    carinfo.append(prompt.kind)
    carinfo.append(prompt.color)
    carinfo.append(prompt.value)

# making a clear function to clear the console
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux
    else:
        _ = system('clear')

db = sqlite3.connect("carDB.sqlite3")
cursor = db.cursor()

carList = []

# Automatically creates a new table in the database if there are none existing already.
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cars' ''')
if cursor.fetchone()[0] != 1:
    cursor.execute(
        '''CREATE TABLE cars(id INTEGER PRIMARY KEY, brand TEXT, price INTEGER, year INTEGER, licensePlate TEXT, 
        isLeasingCar BOOLEAN)''')
    carList.append(Car("Mercedes", 950000, 2018, "AB07354", 1))
    carList.append(Car("Citroën", 60000, 2013, "B012345", 0))
    carList.append(Car("BMW", 567000, 2020, "SC60856", 0))

    for c in carList:
        cursor.execute(''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                       (c.brand, c.price, c.year, c.licensePlate, c.isLeasingCar))
        db.commit()


def intro():
    clear()
    cursor.execute("SELECT COUNT (*) FROM cars")
    rowcount = cursor.fetchone()[0]
    print("There is ", rowcount, " cars in the database.")
    print("1. Pick a car")
    print("2. Add a car")
    print("3. Remove a car")
    print("4. Update a car")
    print("5. Pick a car to continue")
    print("6. Exit")
    choice = get_numeric_input("What do you choose? Enter number\n")
    if choice == 1:
        showOne()
    elif choice == 2:
        add()
    elif choice == 3:
        remove()
    elif choice == 4:
        update()
    elif choice == 5:
        showAll()
    elif choice == 6:
        print("Saving cars and exiting program")
        sys.exit
    else:
        print("This is not an option")
        input("Press enter to continue")
        intro()


def showAll():
    clear()
    cur = cursor.execute("SELECT * from cars")
    t = PrettyTable(["ID", "Brand", "Price [kr.]", "Year", "License plate", "Is car leased?"])
    for row in cur:
        if row[5]:
            leasing = "Yes"
        else:
            leasing = "No"
        t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
    print(t)
    input("Press enter to continue")
    intro()


def add():
    clear()
    print('What is the brand of the car? Write "a" to cancel\n')
    brandInput = input('Or write "i" to import a car from bilhandel.dk\n')
    if brandInput.lower() == "a":
        intro()
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

                licensePlateInput = input("What is the license plate if the car?\n")
                isLeasingCarInput = input("Is the car leased?\n").lower()
                if isLeasingCarInput.startswith("j" or "y"):
                    cursor.execute(
                        ''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                        (title, priceOutput, yearOutput, licensePlateInput, 1))
                else:
                    cursor.execute(
                        ''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                        (title, priceOutput, yearOutput, licensePlateInput, 0))
                db.commit()
                intro()
    else:
        priceInput = get_numeric_input(input('What is the price of the car?\n'))
        
        yearInput = get_numeric_input("What year is the car from?\n"))
    
        licensePlateInput = input("What is the license plate if the car?\n")
        isLeasingCarInput = input("Is the car leased?\n").lower()
        if isLeasingCarInput in yeslist:
            cursor.execute(''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                           (brandInput.capitalize(), priceInput, yearInput, licensePlateInput, 1))
        else:
            cursor.execute(''' INSERT INTO cars(brand, price, year, licensePlate, isLeasingCar) VALUES (?,?,?,?,?) ''',
                           (brandInput.capitalize(), priceInput, yearInput, licensePlateInput, 0))
        db.commit()
        intro()


def remove():
    clear()
    cur = cursor.execute("SELECT id, brand, price, year, licensePlate, isLeasingCar from cars")
    t = PrettyTable(["ID", "Brand", "Price [kr.]", "Year", "License plate", "Is car leased?"])
    for row in cur:
        if row[5]:
            leasing = "Ja"
        else:
            leasing = "Nej"
        t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
        '''print(str(row[0]) + ".", row[1], "fra år ", row[2], "med nummepladen:", row[3])'''
    print(t)
    print('What car do you want to remove? Enter ID')
    carID = input('Write "a" to cancel\n')
    if carID.lower() == "a":
        intro()
    else:
        switch = 0
        while switch == 0:
            try:
                float(carID)
            except ValueError:
                clear()
                print("This is not a number")
                input("Press enter to continue")
                remove()
            else:
                switch = 1
        sqlDelete = '''DELETE from cars where id=?'''
        sqlData = (int(carID))
        cursor.execute(sqlDelete, (int(sqlData),))
        db.commit()
        intro()


def update():
    clear()
    cur = cursor.execute("SELECT id, brand, price, year, licensePlate, isLeasingCar from cars")
    t = PrettyTable(["ID", "Brand", "Price [kr.]", "Year", "License plate", "Is car leased?"])
    for row in cur:
        if row[5]:
            leasing = "Yes"
        else:
            leasing = "No"
        t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
    print(t)
    print('What car do you want to update? Enter ID')
    carID = input('Write "a" to cancel\n')
    if carID.lower() == "a":
        intro()
    else:
        switch = 0
        while switch == 0:
            try:
                float(carID)
            except ValueError:
                clear()
                print("This is not a number")
                input("Press enter to continue")
                update()
            else:
                switch = 1
        switch1 = 0
        while switch1 == 0:
            sqlUpdate = ''' SELECT * from cars WHERE id =?'''
            sqlData = (int(carID))
            cur = cursor.execute(sqlUpdate, (int(sqlData),))
            clear()
            for row in cur:
                print("1. Brand:", row[1])
                print("2. Price:", row[2])
                print("3. Year:", row[3])
                print("4. License plate:", row[4])
                if row[5] == 0:
                    print("5. Leasing status: The car is not leased")
                else:
                    print("5. Leasing status: The car is leased")
                print("6. Exit")
            userInput = input("What do you want to update? Enter number\n")
            switch1 = 1
            switch2 = 0
            while switch2 == 0:
                try:
                    float(userInput)
                except ValueError:
                    clear()
                    print("This is not a number")
                    input("Press enter to continue")
                else:
                    switch2 = 1
            if int(userInput) == 1:
                clear()
                sqlUpdate = ''' UPDATE cars SET brand =? WHERE id =? '''
                sqlData = input("What is the new brand for the car?\n")
                cursor.execute(sqlUpdate, (sqlData, int(carID),))
                db.commit()
            if int(userInput) == 2:
                clear()
                sqlUpdate = ''' UPDATE cars SET price =? WHERE id =? '''
                switch3 = 0
                while switch3 == 0:
                    sqlData = input("What is the new price for the car?\n")
                    try:
                        float(sqlData)
                    except ValueError:
                        clear()
                        print("This is not a number")
                        input("Press enter to continue")
                    else:
                        switch3 = 1
                cursor.execute(sqlUpdate, (int(sqlData), int(carID),))
                db.commit()
            if int(userInput) == 3:
                clear()
                sqlUpdate = ''' UPDATE cars SET year =? WHERE id =? '''
                switch4 = 0
                while switch4 == 0:
                    sqlData = input("What is the new year for the car?\n")
                    try:
                        float(sqlData)
                    except ValueError:
                        clear()
                        print("This is not a number")
                        input("Press enter to continue")
                    else:
                        switch4 = 1
                cursor.execute(sqlUpdate, (int(sqlData), int(carID),))
                db.commit()
            if int(userInput) == 4:
                clear()
                sqlUpdate = ''' UPDATE cars SET licensePlate =? WHERE id =? '''
                sqlData = input("What is the new license plate for the car?\n")
                cursor.execute(sqlUpdate, (sqlData, int(carID),))
                db.commit()
            if int(userInput) == 5:
                clear()
                sqlUpdate = ''' UPDATE cars SET isLeasingCar =? WHERE id =? '''
                sqlData = input("Is the car leased?\n").lower()
                if sqlData.startswith("j" or "y"):
                    sqlData = 1
                else:
                    sqlData = 0
                cursor.execute(sqlUpdate, (int(sqlData), int(carID),))
                db.commit()
            if int(userInput) == 6:
                clear()
                switch = 1
        update()


def showOne():
    carinfo = [] 
    clear()
    sqlSearch = ''' SELECT * from cars WHERE brand =?'''
    sqlData = (input("Search for car brand: "))
    cur = cursor.execute(sqlSearch, (sqlData.capitalize(),))
    if cur.fetchone():
        clear()
        cur = cursor.execute(sqlSearch, (sqlData.capitalize(),))
        t = PrettyTable(["ID", "Brand", "Price [usd.]", "Year", "License plate", "Is car leased?"])
        print("Showing results for", sqlData)
        for row in cur:
            if row[5]:
                leasing = "Yes"
            else:
                leasing = "No"
            t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
        print(t)
        carpick = input("Is this car correct?")
        if carpick in yeslist:
            carlist.append(row[0], row[1], row[2], row[3])
            return carlist
    else:
        clear()
        print("There was no results for the brand", sqlData + ".")
        userInput = input("Do you want to add a new car?\nPress a\nDo you want to restart?\nPress r\nOtherwise Press Enter to continue").lower()
        if userInput == "a":
            add()
        elif userInput == "r":
            showOne()
        else:
            intro()


db.commit()
db.close()


# Code from https://www.learnpython.org/en/Classes_and_Objects
#class Vehicle:
    #name = ""
    #kind = "car"
    #color = ""
    #value = 100.00
    #def description(self):
        #desc_str = "%s %s that is named %s and has a value of %.2f" % (self.color, self.kind, self.name, self.value)
        #return desc_str
    #def info(self):
        #return self.name, self.kind, self.color, self.value


try:
    with open(savepath / 'carinfo.pkl', 'rb') as f:
        carinfo = pickle.load(f)
except FileNotFoundError:
    print("There is no saved data for this program")

while True:
    if not carinfo:
        time.sleep(2)
        print("Please add your car")
        time.sleep(2)
        car1 = Vehicle()
        car1.name = caps("What is the name of your car?")
        car1.kind = input("What kind of car do you have?")
        car1.color = input("What is the color of your car?")
        car1.value = get_numeric_input("What is the value of the car?")
        print("Is your car a " + car1.description())
        iinp = input()
        if iinp.lower() in yeslist:
            savetolist(car1)
            car = car1
            break
        else:
            continue
    else:
        newcar = input("Do you want to create a new car?")
        if newcar.lower() in yeslist:
            while True:
                newcar = str(len(carinfo) // 4 + 1)
                print("Please add your car")
                time.sleep(2)
                newcar = Vehicle()
                newcar.name = caps("What is the name of your car?")
                newcar.kind = input("What kind of car do you have?")
                newcar.color = input("What is the color of your car?")
                newcar.value = get_numeric_input("What is the value of the car?")
                print("Is your car a " + newcar.description())
                iinp = input()
                if iinp.lower() in yeslist:
                    savetolist(newcar)
                    car = newcar
                    break
                else:
                    continue
        else:
            carinput = get_numeric_input("Pick the car you want to use in the order it is shown in")
            
            i = 0
            for i in range(0, len(carinfo), 4):
                print(carinfo[i])
                i += 4
            carinput = (carinput-1)*4
            car = carinfo[carinput]
            print(f"Your current car is {car}")
            break

ecount = 0
while True:
    print("Saving Data")
    try:
        with open(savepath / 'carinfo.pkl', 'wb') as f:
            pickle.dump(carinfo, f)
    except Exception as e:
        ecount += 1
        print(f"An error occurred: {e}. Attempt {ecount}")
    else:
        print("File Save Successful!")
        break
    finally:
        if ecount >= 60:
            quitput = input("Do you want to quit trying to save?\nThis will mean that any new data will be lost.")
            if quitput.lower() in yeslist:
                break
print("Thank you for setting up you car")
time.sleep(2)
print("You may now calculate how long it will take for your car to reach it's destination and how far the destination is")
time.sleep(2)
#distance calc
#pos inputs
carpos = []
carx = get_numeric_input("What is your car's starting X position?")
carpos.append(carx)
cary = get_numeric_input("What is your car's starting Y position?")
carpos.append(cary)
des = get_numeric_input("Input your destination's X position")
des1 = get_numeric_input("Input your destination's Y position")
#calc
des = int(des) - int(carpos[0])
des1 = int(des1) - int(carpos[1])

# Integer Fix
des = abs(des)
des1 = abs(des1)
    
des = des + des1

# What happens if the distance to get somewhere is 0

if des == 0:
    print("Why did you input the same coordinates twice?")
    print("Well as a punishment you ain't gonna be using this program")
    print("Better luck next time!")
    sys.exit()
print(f"Your car will have to drive {des} blocks to reach your destination!")

#block to mile
miles = des / 20

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
for threshold, coefficient in sorted(value_coefficients.items(), reverse=True):
    if car.value >= threshold:
        ime = coefficient * des
        break
else:
    ime = 5 * des

print(f"It wil take {ime} minutes to arrive at your destination")

# gas calc
speedword = []
while True:
    sped = input("How fast do you want to go?\nFast?\nMedium?\nSlow?")
    spedwords = {
        'fast': 10,
        'medium': 35,
        'slow': 65,
    }
    for word, co in spedwords.items():
        if word in sped.lower():
            gas = miles / co
            speedword.append(co)
            speedword_str = str(speedword)
            break
    else:
        print("Invalid speed input. Please choose from 'Fast', 'Medium', or 'Slow'.")
        continue

    print(f"You will use {gas} gallons")
    print(f"In other words, you will use {speedword} miles per gallon")
    break
