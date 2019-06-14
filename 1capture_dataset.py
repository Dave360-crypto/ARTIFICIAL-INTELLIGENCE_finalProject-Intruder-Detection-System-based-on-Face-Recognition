import face_recognition
import sqlite3
import glob
import cv2
import os
from playsound import playsound

IP_Webcam = False
flag = False

if IP_Webcam is True:
    video_capture = cv2.VideoCapture('http://192.168.0.16:8080/videofeed') # IP Webcam
else:
    video_capture = cv2.VideoCapture(0)

db = sqlite3.connect('aiProject.sqlite3')
print("Opened Database Successfully !!")

cursor = db.cursor()

# Create database
cursor.execute('''CREATE TABLE IF NOT EXISTS AI_PROJECT
            (FACE_ID  INTEGER  PRIMARY KEY  AUTOINCREMENT,
            FACE_NAME    TEXT  NOT NULL,
            FACE_ENCODING   blob  NOT NULL );''')

while(True):
    ret, frame = video_capture.read()

    cv2.imshow('Press "C" to Capture Face and KeyIn Name in terminal ', frame)
    flag = False

    c = cv2.waitKey(1)
    if 'q' == chr(c & 255):
        print("Exited Operation !!")
        exit()

    if 'c' == chr(c & 255):
        unknown_face_encodings = face_recognition.face_encodings(frame)
        if len(unknown_face_encodings) > 0:
            while(flag == False):
		#print("Press c to capture!!")
                print("Please enter your Name : ")
                name = str(input())
                cursor.execute("SELECT count(*) FROM AI_PROJECT WHERE FACE_NAME = ?", (name, ))
                data = cursor.fetchone()[0]
                if data == 0:
                    file_name = name + ".jpg"
                    cv2.imwrite(file_name, frame)
                    face_encoding = unknown_face_encodings[0]
                    break
                    
                else:
                    print("Name Already Exists, want to enter another Name ? (Y/N)")
                    s = str(input()).lower()
                    if s == 'y':
                        continue
                    elif s == 'n':
                        file_name = name + ".jpg"
                        cv2.imwrite(file_name, frame)
                        face_encoding = unknown_face_encodings[0]
                        break
                    elif s == 'e':
                        print("Exited Operation !!")
                        exit()
            if flag == False:
                break

        else:
            print("There's no face recognized in the image !!")

    if 's' == chr(c & 255):
        flag = True
        break

if IP_Webcam is not True:
    video_capture.release()
cv2.destroyAllWindows()

# Insert Operation
if flag is False:
    cursor.execute("SELECT count(*) FROM AI_PROJECT WHERE FACE_NAME = ?", (name, ))
    data = cursor.fetchone()[0]
    if data == 0:
        cursor.execute("INSERT INTO AI_PROJECT (FACE_NAME, FACE_ENCODING) VALUES (?, ?)",
                (name, sqlite3.Binary(face_encoding)))
        print("Photo Captured Successfully !!")
    else:
        cursor.execute("DELETE FROM AI_PROJECT WHERE FACE_NAME = ?", (name, ))
        cursor.execute("INSERT INTO AI_PROJECT (FACE_NAME, FACE_ENCODING) VALUES (?, ?)",
                (name, sqlite3.Binary(face_encoding)))
        print("Photo Overwritten Successfully !!")

# Database Update Operation
print("Updating the Database !!")
playsound('sound.mp3')
for img in sorted(glob.glob("*.jpg")):
    img_name = os.path.basename(img)[:-4]
    cursor.execute("SELECT count(*) FROM AI_PROJECT WHERE FACE_NAME = ?", (img_name, ))
    data = cursor.fetchone()[0]
    if data == 0:
        image = face_recognition.load_image_file(img)
        image_encoding = face_recognition.face_encodings(image)
        if len(image_encoding) > 0:
            cursor.execute("INSERT INTO AI_PROJECT (FACE_NAME, FACE_ENCODING) VALUES (?, ?)",
                        (img_name, sqlite3.Binary(image_encoding[0])))

db.commit()
print("Done !!")
db.close()
