#UNUSED MODULE
import pickle
#module used across the code for dramatic effect
import time
i = 0
yeslist = ["yes","y","of course"]
#code from https://www.learnpython.org/en/Classes_and_Objects
class Vehicle:
    name = ""
    kind = "car"
    color = ""
    value = 100.00
    def description(self):
        desc_str = "%s %s that is named %s and has a value of %f" % (self.color, self.kind, self.name, self.value)
        return desc_str
    def info(self):
        return self.name, self.kind, self.color, self.value
carinfo = []
while i == 0:
    if carinfo != "":
        print("There is no saved data for this program")
        time.sleep(2)
        print("Please add your car")
        time.sleep(2)
        car1 = Vehicle()
        car1.name = input("What is the name of your car?")
        car1.kind = input("What kind of car do you have?")
        car1.color = input("What is the color of your car?")
        car1.value = input("What is the value of the car?")
        car1.value = int(car1.value)
        print("Is your car a " + car1.description())
        for i in yeslist:
            iinp = input()
            if iinp in yeslist:
                carinfo.append(car1.info)
                car = car1
                break
            else:
                break
    else:
        print(carinfo)
        break
print("Thank you for setting up you car")
time.sleep(2)
print("You may now calculate how long it will take for your car to reach it's destination and how far the destination is")
time.sleep(2)
#distance calc
#pos inputs
carpos = []
carx = input("What is your car's starting X position?")
carpos.append(carx)
cary = input("What is your car's starting Y position?")
carpos.append(cary)
des = input("Input your destination's X position")
des1 = input("Input your destination's Y position")
#calc
des = int(des) - int(carpos[0])
des1 = int(des1) - int(carpos[1])
des = des + des1
#module import for this part of code
import sys
#Integer fix
if des < 0:
    des = des * -1
elif des == 0:
    print("Why did you input the same coordinates twice?")
    print("Well as a punishment you ain't gonna be using this program")
    print("Better luck next time!")
    sys.exit()
print(f"Your car will have to drive {des} blocks to reach your destination!")
#car time calc
if car.value >= 100000:
    ime = 0.1 * des
elif car.value >= 50000 :
    ime = 0.75 * des
elif car.value >= 25000:
    ime = 1 * des
elif car.value >= 10000:
    ime = 1.25 * des
elif car.value >= 5000:
    ime = 1.6 * des
elif car.value >= 1000:
    ime = 2 * des
else:
    ime = 5 * des
print(f"It wil take {ime} minutes to arrive at your destination")