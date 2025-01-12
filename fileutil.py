import shutil

class FileUtil:
    def __init__(self):
        pass

    def readLine(self, index):
        print(index)
        if index == False:
            try:
                shutil.copy("temp.jpg", "static/media/temp.jpg")
            except:
                pass
            return "False"
        else:
            peopleFile = open("med_info.txt", "r")
            people = []
            for line in peopleFile:
                people.append(line)
            try:
                returnStatement = people[int(index)]
                shutil.copy(f"{returnStatement.split(',')[0]}.jpg", "static/media/temp.jpg")
            except:
                peopleFile.close()
                return "False"
            peopleFile.close()
            print(returnStatement)
            return returnStatement
    
    def updateLine(self, newLine):
        peopleFile = open("med_info.txt", "r")
        people = []
        for line in peopleFile:
            people.append(line)
        peopleFile.close()
        f = open("temp.txt", 'r')
        index = f.read()
        f.close()
        print(people)
        people[people.index(index)] = newLine + "\n"
        f = open("temp.txt", "w")
        f.write(newLine + "\n")
        f.close()
        peopleFile = open("med_info.txt", "w")
        for item in people:
            peopleFile.write(item)
        peopleFile.close()

    def newLine(self, newLine):
        peopleFile = open("med_info.txt", "r")
        people = []
        for line in peopleFile:
            people.append(line)
        peopleFile.close()
        people.append(newLine + "\n")
        f = open("temp.txt", "w")
        f.write(newLine + "\n")
        f.close()
        peopleFile = open("med_info.txt", "w")
        for item in people:
            peopleFile.write(item)
        peopleFile.close()

    def saveImage(self, newLine):
        identifier = newLine.split(',')[0]
        try:
            shutil.copy("static/media/temp.jpg", f"{identifier}.jpg")
        except:
            pass