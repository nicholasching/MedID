import os
from google import genai
from google.genai import types
from dotenv import load_dotenv, dotenv_values

load_dotenv()
model = genai.Client(api_key=os.environ["API_KEY"])

# Hashcode, Name
mimeType = 'image/jpeg'
peopleFile = open("people.txt", "r")
images_bytes = []
for line in peopleFile:
    try:
        with open(f"{line.split(",")[0].rstrip("\n")}.jpg", "rb") as f:
            images_bytes.append(f.read())
    except:
        print(f"Error: {line.split(",")[0]}.jpg has not been found")
peopleFile.close()

response = model.models.generate_content(model='gemini-2.0-flash-exp', contents=[
    types.Part.from_text('Which image does the last image best resemble? Simply output the index of image, starting with index 0.'),
    [types.Part.from_bytes(data=images_bytes[i], mime_type=mimeType)
    for i in range(len(images_bytes))]
])
print(response.text)