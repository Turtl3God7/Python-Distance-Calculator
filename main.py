# Module used across code to gain info about client operating system
import os
# Module used for forcefully ending the program
import sys
# Module used across the code for dramatic effect
import time
# SQL module
import sqlite3
# Module used to make SQl tables prettier
from prettytable import PrettyTable
# Import from support file "Car.py"
from Car import Car
# Data Scraper for SQL table add() function
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


# Yes List with the Extension Plus Feature
# Note: Would be easier if we find a module to do this for us (looks kinda messy)
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


# making a clear function to clear the console
name = os.name
def clear():
    if name == 'nt':
        os.system('cls')
    # for mac and linux
    else:
        os.system('clear')

db = sqlite3.connect("carDB.sqlite3")
cursor = db.cursor()

carList = []
carlist = []

def intro():
    clear()
    cursor.execute("SELECT COUNT (*) FROM cars")
    rowcount = cursor.fetchone()[0]
    print("There is ", rowcount, " cars in the database.")
    print("1. Pick a car to continue")
    print("2. Add a car")
    print("3. Remove a car")
    print("4. Update a car")
    print("5. Show all cars")
    print("6. Exit")
    userInput = input("What do you choose? Enter number\n")
    switch = 0
    while switch == 0:
        try:
            int(userInput)
        except ValueError:
            clear()
            print("This is not a number")
            input("Press enter to continue")
            intro()
        else:
            switch = 1
    choice = int(userInput)
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
        clear()
        print("Saving cars and exiting program")
        sys.exit()
    else:
        print("This is not an option")
        input("Press enter to continue")
        intro()


def showAll():
    clear()
    cur = cursor.execute("SELECT * from cars")
    t = PrettyTable(["ID", "Brand", "Price [usd.]", "Year", "Car Type", "Is car leased?"])
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

                cartypeInput = input("What type of car is it?\n")
                isLeasingCarInput = input("Is the car leased?\n").lower()
                if isLeasingCarInput.startswith("j" or "y"):
                    cursor.execute(
                        ''' INSERT INTO cars(brand, price, year, cartype, isLeasingCar) VALUES (?,?,?,?,?) ''',
                        (title, priceOutput, yearOutput, cartypeInput, 1))
                else:
                    cursor.execute(
                        ''' INSERT INTO cars(brand, price, year, cartype, isLeasingCar) VALUES (?,?,?,?,?) ''',
                        (title, priceOutput, yearOutput, cartypeInput, 0))
                db.commit()
                intro()
    else:
        switch = 0
        while switch == 0:
            try:
                priceInput = float(input('What is the price of the car?\n'))
            except ValueError:
                clear()
                print("This is not a number")
                input("Press enter to continue")
            else:
                switch = 1
        switch = 0
        while switch == 0:
            try:
                yearInput = int(input("What year is the car from?\n"))
            except ValueError:
                clear()
                print("This is not a number")
                input("Press enter to continue")
            else:
                switch = 1
        cartypeInput = input("What type of car is it?\n")
        isLeasingCarInput = input("Is the car leased?\n").lower()
        if isLeasingCarInput.startswith("j" or "y"):
            cursor.execute(''' INSERT INTO cars(brand, price, year, cartype, isLeasingCar) VALUES (?,?,?,?,?) ''',
                           (brandInput.capitalize(), priceInput, yearInput, cartypeInput, 1))
        else:
            cursor.execute(''' INSERT INTO cars(brand, price, year, cartype, isLeasingCar) VALUES (?,?,?,?,?) ''',
                           (brandInput.capitalize(), priceInput, yearInput, cartypeInput, 0))
        db.commit()
        intro()


def remove():
    clear()
    cur = cursor.execute("SELECT id, brand, price, year, cartype, isLeasingCar from cars")
    t = PrettyTable(["ID", "Brand", "Price [usd.]", "Year", "Car Type", "Is car leased?"])
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
    cur = cursor.execute("SELECT id, brand, price, year, cartype, isLeasingCar from cars")
    t = PrettyTable(["ID", "Brand", "Price [usd.]", "Year", "Car Type", "Is car leased?"])
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
                print("4. Car Type:", row[4])
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
                sqlUpdate = ''' UPDATE cars SET cartype =? WHERE id =? '''
                sqlData = input("What is the updated car type?\n")
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
    clear()
    searchtype = input("Do you want to search by Brand or ID\nPress 'b' for brand or 'i' for ID")
    print("Note, it is recommended to use Brand search first in case if you have multiple cars of the same brand")
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
                if row[5]:
                    leasing = "Yes"
                else:
                    leasing = "No"
            t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
            print(t)
            carpick = input("Is this car correct?")
            if carpick in yeslist:
                carlist.append([row[0], row[1], row[2], row[3], row[4], leasing])
            else:
                caryes = input("Sorry about that\nWould you like to try again press 'a' or restart? press 'r'")
                try:
                    if caryes == "a":
                        showOne()
                except:
                    print("That value isn't accepted")
                else:
                    if caryes == "r":
                        intro()
        else:
            clear()
            print("There was no results for the brand", sqlData + ".")
            userInput = input("Do you want to add a new car?\n").lower()
            print(userInput)
            if userInput in yeslist:
                add()
            else:
                intro()
        intro()
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
                if row[5]:
                    leasing = "Yes"
                else:
                    leasing = "No"
            t.add_row([row[0], row[1], row[2], row[3], row[4], leasing])
            print(t)
            carpick = input("Is this car correct?")
            if carpick in yeslist:
                carlist.append([row[0], row[1], row[2], row[3], row[4], leasing])
            else:
                caryes = input("Sorry about that\nWould you like to try again press 'a' or restart? press 'r'")
                try:
                    if caryes == "a":
                        showOne()
                except:
                    print("That value isn't accepted")
                else:
                    if caryes == "r":
                        intro()
        else:
            clear()
            print("There was no results for the ID", sqlData + ".")
            userInput = input("Do you want to add a new car?\n").lower()
            print(userInput)
            if userInput in yeslist:
                add()
            else:
                intro()
    else:
        print("That is not a valid input")
        clear()
        showOne()

intro()

db.commit()
db.close()


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
    if carlist[3] >= threshold:
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
