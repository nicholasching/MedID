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
                shutil.copy(f"{returnStatement.split(",")[0]}.jpg", "static/media/temp.jpg")
            except:
                peopleFile.close()
                return "False"
            peopleFile.close()
            print(returnStatement)
            return returnStatement
        