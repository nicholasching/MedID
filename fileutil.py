class FileUtil:
    def __init__(self):
        pass

    def readLine(self, index):
        print(index)
        if index == False:
            return "False"
        else:
            peopleFile = open("med_info.txt", "r")
            people = []
            for line in peopleFile:
                people.append(line)
            returnStatement = people[int(index)]
            peopleFile.close()
            print(returnStatement)
            return returnStatement
        