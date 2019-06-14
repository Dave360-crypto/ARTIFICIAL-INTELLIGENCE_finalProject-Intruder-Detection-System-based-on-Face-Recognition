import sqlite3

db = sqlite3.connect('aiProject.sqlite3')
print("Opened Database Successfully !!")

cursor = db.cursor()

print("Do you want to reset the table AI_PROJECT ? (Y/N)")
s = str(input()).lower()
if s == 'y':
    cursor.execute("DELETE FROM AI_PROJECT")
    print("Reset Database Successfully !!")
elif s == 'n':
    print("Exited Operation !!")

db.commit()
db.close()
