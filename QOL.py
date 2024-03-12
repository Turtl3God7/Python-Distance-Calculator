# Here to make VS code not to annoy me (These imports aren't needed)
import os
import sqlite3
from time import sleep
from colorama import just_fix_windows_console
from termcolor import colored


# Yes List with the Extension Plus Feature
# Note: Would be easier if we find a module to do this for us (looks kinda messy) <-- AI generated
yeslist = ["yes","y","of course","yea","okay","yeah","ok","alright","yep","ay","aye",
"positively","all right","yo","certainly","absolutely","exactly","indeed","okeydokey",
"undoubtedly","assuredly","unquestionably","indisputably","all right","alright","very well",
"of course","by all means","sure","certainly","absolutely","indeed","affirmative","in the affirmative",
"agreed","roger","aye","aye aye","yeah","yah","yep","yup","uh-huh","okay","OK","okey-dokey","okey-doke",
"achcha","righto","righty-ho","surely","yea"]

name = os.name
# making a clear function to clear the console
def clear():
    if name == 'nt':
        os.system('cls')
    # for mac and linux
    else:
        os.system('clear')

# advanced numerical checker
def get_numeric_input(prompt, function=None, city: bool = None, maxattempts=9999999999):
    attempts = 0
    while maxattempts > attempts:
        try:
            return int(input(prompt))
        except ValueError:
            attempts += 1
            print("Please enter a valid numerical value.")
            if attempts < 2:
                sleep(1)
                if function:
                    if city == True:
                        function(city)
                    else:
                        function()
                else:
                    clear()
            if attempts >= 2:
                print("Try removing any special characters like commas")
                sleep(1)
                if function:
                    if city == True:
                        function(city)
                    else:
                        function()
                else:
                    clear()
    input("You have hit the max attempts set for this part of the program\nYou will now be sent back to the beginning\n")
    # Consider passing a callback function to handle this scenario.

def caps(prompt):
    prompt = input(prompt)
    prompt = prompt.title()
    return prompt

# save path
current_directory = os.path.dirname(os.path.abspath(__file__))
sql_name = "carDB.sqlite3"
file_path = os.path.join(current_directory, sql_name)


# Function that prints anything in red if there is no value in var
just_fix_windows_console()
def checkcars(message, num):
    if num != 0:
        return print(message)
    else:
        return print(colored(message, "red"))
        

#SQl database setup
db = sqlite3.connect(file_path)
cursor = db.cursor()



#Code to automaticly create a SQL table
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cars' ''')
if cursor.fetchone()[0] != 1:
    cursor.execute(
        '''CREATE TABLE cars(id INTEGER PRIMARY KEY, brand TEXT, price INTEGER, year INTEGER, cartype TEXT, 
        isLeasingCar BOOLEAN)''')
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cache' ''')
if cursor.fetchone()[0] != 1:
    cursor.execute('''CREATE TABLE cache(choosen INTEGER PRIMARY KEY)''')

# Code that adds a comma every 3 digits
def numericformat(prompt, source, index):
    formatted_number = ''
    for i, digit in enumerate(reversed(str(prompt))):
        if i > 0 and i % 3 == 0:
            formatted_number = ',' + formatted_number  # Add comma every 3 digits
        formatted_number = digit + formatted_number
    source.pop(index)
    source.insert(index, formatted_number)
    
def fibonacci(n, cache={}):
    if n <= 0:
        return []
    elif n == 1:
        return [0,1]
    elif n in cache:
        return cache[n]
    else:
        fib_list = [0,1]
        for i in range(2, n + 1):
            fib_list.append(fib_list[-1] + fib_list[-2])
        cache[n] = fib_list
        return fib_list
 