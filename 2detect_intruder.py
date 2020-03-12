import face_recognition
import numpy as np
import requests
import sqlite3
import cv2
import smtplib #saya import smtp library
from playsound import playsound #saya import sound
import gmail_alert #import file gmail alert


IP_Webcam = False

if IP_Webcam is True:
    video_capture = cv2.VideoCapture('http://192.168.0.16:8080/')  # saya cuba implement IP Webcam instead of builtin cam
else:
    video_capture = cv2.VideoCapture(1)

known_face_names = []
known_face_encodings = []

db = sqlite3.connect('aiProject.sqlite3')
print("Opened Database Successfully !!")

cursor = db.cursor()

cursor.execute("SELECT * FROM sqlite_master WHERE name ='AI_PROJECT' and type='table';")
chk = cursor.fetchone()
if chk is not None:
    data = cursor.execute("SELECT FACE_NAME, FACE_ENCODING FROM AI_PROJECT")
else:
    print("There's no face entry in the Database !!")
    exit()

for row in data:
    known_face_names.append(row[0])
    known_face_encodings.append(np.frombuffer(row[1]))

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Intruder"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        height, width, _ = frame.shape
        font = cv2.FONT_HERSHEY_DUPLEX

        if name is not "Intruder":
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, 'Permission Granted !!', (int(width / 4), height - 430), font, 1.0, (255, 255, 255), 1, cv2.LINE_AA)
            #playsound('sound.mp3')
        else:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            
            #time.sleep(3)
           # p.terminate()
           # p.join()
            cv2.putText(frame, 'Intruder Detected !!', (int(width / 4), height - 50), font, 1.0, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, 'System Freezed !!', (int(width / 4), height - 20), font, 1.0, (255, 255, 255), 1, cv2.LINE_AA)
            #if cv2.puttext == ('System Freezed !!')
            playsound('alarmDet(1).mp3')
            open("gmail_alert.py", "r")
            print("Intruder has been detected")

        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    cv2.imshow('Private Space Intrusion Detection System', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exited Operation !!!")
        break
 		


if IP_Webcam is not True:
    video_capture.release()
cv2.destroyAllWindows()
