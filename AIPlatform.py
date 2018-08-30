import sys
import json
import os
import secrets #similar to random
import time

#this is the original code, working on improvements
#new comments added

class Ai:
    def __init__(self, name, firstData = {}):
        self.name = str(name)
        self.firstData = firstData

    def writeMem(self, newMem): #save memory
        try:
            os.mkdir("AIs")
        except FileExistsError:
            pass
        with open("AIs/" + self.name + "_memory.json", "w") as mem:
            json.dump(newMem, mem)

    def readMem(self): #load memory
        try:
            with open("AIs/" + self.name + "_memory.json", "r") as mem:
                loadedMem = json.load(mem)
        except FileNotFoundError:
            print("My memory is empty.")
            self.writeMem(self.firstData)
            return self.readMem()
        return loadedMem

    def learn(self, obj = ""): #save input to memory
        loadedMem = self.readMem()
        if obj == "":
            print("(By the way, I can also learn from another AI, " +
            "just write it's name.)")
            obj = input("Name of the object: ")

        if obj in human.loadedUser["ais"]: #learn from other AI
            aiCode = human.loadedUser["ais"][obj]
            aiMem = globals()[aiCode].readMem()
            aiKeys = list(aiMem.keys())
            for i in aiKeys:
                if i not in loadedMem:
                    loadedMem[i] = aiMem[i]
            self.writeMem(loadedMem)
            return

        if obj in loadedMem: #already in memory
            decide = input("According to my memory " + obj + " is " +
            str(loadedMem[obj]) + ".\nDo you want me to keep, " +
            "overwrite or forget it? [keep/overwrite/forget]\n")
            while True:
                if decide == "keep":
                    return
                elif decide == "forget":
                    del loadedMem[obj]
                    self.writeMem(loadedMem)
                    return
                elif decide != "overwrite":
                    decide = input("Sorry, I don't understand. Do you wish " +
                    "to keep, " + "overwrite or forget " + obj + "?")
                if decide in ["overwrite", "forget", "keep"]:
                    break

        information = input("Description of the object: ")
        loadedMem[obj] = information
        self.writeMem(loadedMem)

    def recall(self): #load and print from memory
        loadedMem = self.readMem()
        print('To print my entire memory input "print memory".')
        request = input("Name of the object: ")

        if request == "print memory":
            print(loadedMem)
            print('Please don\'t delete my entire memory by writing ' +
            '"delete memory".\n')
        elif request in loadedMem:
            result = loadedMem[request]
            print(result)
        elif request == "name":
            print("My default name is " + self.name + ".")
        else:
            print("No such object in memory. Could you describe it for me?")
            self.learn(request)

    def speak(self): #load and print randomly from memory
        loadedMem = self.readMem()
        try:
            chosenKey = secrets.choice(list(loadedMem.keys()))
        except IndexError:
            return
        else:
            print(chosenKey + " is " + loadedMem[chosenKey])

    def wait(self): #do nothing for x seconds
        howLong = float(input("How long should I wait?\n"))
        if howLong > 99:
            confirm = input("That is very long, are you sure? [y/n]\n")
            if confirm in ["n", "no"]:
                return
        time.sleep(howLong)

    def deleteMem(self):
        print("DELETING MEMORY...")
        try:
            os.remove("AIs/" + aiName + "Memory.json") #maybe full path is required, didn't have time to check that
            print("Nooo, my knowledge is lost forever :(.")
        except FileNotFoundError:
            pass

class User:
    def __init__(self):
        self.userName = ''
        self.password = ''
        self.logIn()
        self.loadedUser = {self.userName: self.password, "creations": 0, "numOfAis": 0}
        self.findUser()

        l = 0
        while self.password != self.loadedUser[self.userName]:
            print("Incorrect password.")
            self.logIn()
            if l > 8:
                print("You have unsuccesfully attempted to log in " +
                "too many times, the program will now exit.")
                time.sleep(1)
                sys.exit()
            l += 1

        print("====================")
        print("Available AIs:")
        print(list(self.loadedUser["ais"].keys()))
        self.commands = ["learn", "recall", "speak", "wait", "create",
        "destroy", "quit", "whatever"]
        print("--------------------")
        print("Commands for AI:")
        print(self.commands)
        print("--------------------")

    def logIn(self):
        print("--------------------")
        self.userName = input("Username: ")
        self.password = input("Password: ")
        if "quit" in [self.userName, self.password]:
            sys.exit()

    def saveUser(self):
        try:
            os.mkdir("Users")
        except FileExistsError:
            pass
        with open("Users/" + self.userName + "_user.json", "w") as mem:
            json.dump(self.loadedUser, mem)

    def findUser(self):
        try:
            with open("Users/" + self.userName + "_user.json", "r") as mem:
                self.loadedUser = json.load(mem)
        except FileNotFoundError:
            print("New user: " + self.userName + "\nWelcome!")
            self.createAis()
            return self.findUser()
        else:
            self.recreateAis()

    def createAis(self): #create new AIs
        while True:
            try:
                numOfAis = int(input("How many AIs do you want?\n"))
            except TypeError:
                print("Please input an integer.")
            else:
                break

        if not numOfAis:
            inp = input('You have no available AIs at the moment.\n' +
            'Type "create" to create new AIs or anything else to exit.')
            if inp == "create":
                self.createAis()
            else:
                sys.exit()

        ais = {}
        defaultNames = ["Louie", "Arooj", "Avani"]

        for i in range(numOfAis):
            newName = input("Name your AI (No. " + str(i+1) + "): ")
            if newName == "default": #default names (useful for testing)
                for i in range(numOfAis):
                    globals()[self.userName + "_ai" +
                    str(self.loadedUser["creations"]) + "-" +
                    str(i+1)] = Ai(defaultNames[i])
                    ais[defaultNames[i]] = self.userName + "_ai" + str(self.loadedUser["creations"]) + "-" + str(i+1)
                break
            globals()[self.userName + "_ai" + str(self.loadedUser["creations"])
            + "-" + str(i+1)] = Ai(newName)
            ais[newName] = self.userName + "_ai" + str(self.loadedUser["creations"]) + "-" + str(i+1)

        self.loadedUser["numOfAis"] += numOfAis
        self.loadedUser["ais"] = ais
        self.loadedUser["creations"] += 1
        self.saveUser()

    def recreateAis(self):
        names = list(self.loadedUser["ais"].keys())
        for i in range(self.loadedUser["numOfAis"]):
            globals()[self.loadedUser["ais"][names[i]]] = Ai(names[i])

    def destroyAi(self, ai): #newest and weirdest function... not working properly
        print("DESTROYING AI...")
        ai.deleteMem()
        globals()[self.loadedUser["ais"][ai.name]] = None
        del self.loadedUser["ais"][ai.name]
        self.loadedUser["numOfAis"] -= 1
        self.saveUser()

        otherAis = list(human.loadedUser["ais"].keys())
        if otherAis != []:
            return globals()[human.loadedUser["ais"][secrets.choice(otherAis)]]
        else:
            inp = input('You have no available AIs at the moment.\n' +
            'Type "create" to create new AIs or anything else to exit.')
            if inp == "create":
                self.createAis()
            else:
                sys.exit()

human = User()

while True:
    aiName = input("AI's name: ")
    if aiName in human.loadedUser["ais"]:
        currentAi = globals()[human.loadedUser["ais"][aiName]]
        print("(Write a different AI's name to switch between them.)")
        break
    else:
        print("You have not created any AI with this name yet.")

while True:
    command = input("What should I do? [Current AI: " + currentAi.name + "]\n")

    while command in human.loadedUser["ais"]:
        aiName = command
        currentAi = globals()[human.loadedUser["ais"][aiName]]
        command = input("What should I do? [Current AI: " + currentAi.name + "]\n")

    if command == "whatever": #choose a random command
        command = secrets.choice(human.commands)

    if command == "learn":
        currentAi.learn()
    elif command == "recall":
        currentAi.recall()
    elif command in ["quit", "q"]:
        break
    elif command == "wait":
        currentAi.wait()
    elif command == "speak":
        currentAi.speak()
    elif command == "create":
        human.createAis()
    elif command == "destroy":
        currentAi = human.destroyAi(currentAi)
    elif command == "delete memory":
        currentAi.deleteMem()
    else:
        print("No such command available.")
