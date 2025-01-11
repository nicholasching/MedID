'''ARRAY LAYOUT:
*row = person
*column = info

hashcode, first name, last name, birth year, birth month, birth day, gender, weight, height, blood type, [medical conditions], [current medication],  DNR, *medical history, address, [emergency contact], insurance, last update

*medical history will either be a list or textfile, will add late
'''

info=open('med_info.txt','r')
info=info.read()
database=[]

patient=info.split("\n")

for entry in patient:
    database.append(entry.split(","))

for i in range(len(database)):
    for j in range(len(database[i])): 
        if ";" in database[i][j]:
            database[i][j] = database[i][j].split(";") 

print(database) 
