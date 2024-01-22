yeslist = ("yes","y","of course","yea")

def get_numeric_input(prompt):
    attempts= 0
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid numerical value.")
            attempts += 1
            if attempts >= 1:
                print("Try removing any special characters like commas")
            
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
while True:
    if carinfo != "":
        print("There is no saved data for this program")
        time.sleep(2)
        print("Please add your car")
        time.sleep(2)
        car1 = Vehicle()
        car1.name = input("What is the name of your car?")
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
