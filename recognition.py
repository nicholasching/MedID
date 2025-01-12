import os
from google import genai
from google.genai import types
from dotenv import load_dotenv, dotenv_values

class Recognition:
    def __init__(self):
        load_dotenv()
        self.model = genai.Client(api_key=os.environ["API_KEY"])
        self.mimeType = 'image/jpeg'

    def loadImages(self):
        peopleFile = open("med_info.txt", "r")
        self.images_bytes = []
        for line in peopleFile:
            try:
                with open(f"{line.split(',')[0].rstrip('\n')}.jpg", "rb") as f:
                    self.images_bytes.append(f.read())
            except:
                print(f"Error: {line.split(',')[0]}.jpg has not been found")
        peopleFile.close()

    def processNew(self):
        try:
            with open("temp.jpg", "rb") as f:
                self.images_bytes.append(f.read())
        except:
            print("Error: temp.jpg has not been found")
        
        newIndex = self.runIdent()

        if int(newIndex) == -1:
            return False
        else:
            self.images_bytes.pop()
            return newIndex
        
    def discardNew(self):
        self.images_bytes.pop()

    def runIdent(self):
        response = self.model.models.generate_content(model='gemini-2.0-flash-exp', contents=[
            types.Part.from_text('Return the index of the image, starting at 0, of the person that matches the last image. If a near perfect match is not found, output -1.'),
            [types.Part.from_bytes(data=self.images_bytes[i], mime_type=self.mimeType)
            for i in range(len(self.images_bytes))]
        ])
        return response.text