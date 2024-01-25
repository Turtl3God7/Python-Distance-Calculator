# Module for data serialization of a list
import pickle
# Module used for forcefully ending the program
import sys
#module used across the code for dramatic effect
import time

yeslist = ("yes","y","of course","yea")

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
# Code from https://www.learnpython.org/en/Classes_and_Objects
class Vehicle:
    name = ""
    kind = "car"
    color = ""
    value = 100.00
    def description(self):
        desc_str = "%s %s that is named %s and has a value of %.2f" % (self.color, self.kind, self.name, self.value)
        return desc_str
    def info(self):
        return self.name, self.kind, self.color, self.value
carinfo = [] 

try:
    with open('carinfo.pkl', 'rb') as f:
        carinfo = pickle.load(f)
except FileNotFoundError:
    print("There is no saved data for this program")

while True:
    if carinfo != "":
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
        if iinp in yeslist:
            carinfo.append(car1.info)
            car = car1
            break
        else:
            continue
    else:
        print(carinfo)
        break

while True:
    print("Saving Data")
    try:
        with open('carinfo.pkl', 'wb') as f:
            pickle.dump(carinfo, f)
            f.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()
    else:
        print("File Save Successful!")
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
des = abs(des1)
des1 = abs(des1)
des = des + des1

#0 problem

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
            str(speedword)
            break
    else:
        print("Invalid speed input. Please choose from 'Fast', 'Medium', or 'Slow'.")
        continue

    print(f"You will use {gas} gallons")
    print(f"In other words, you will use {speedword} miles per gallon")
    break
