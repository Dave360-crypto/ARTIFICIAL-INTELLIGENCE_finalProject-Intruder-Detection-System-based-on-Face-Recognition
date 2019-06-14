import face_recognition
import cv2
import numpy as np
from playsound import playsound

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


# Get a reference to webcam #0 (the default one)
#video_capture = cv2.VideoCapture('http://192.168.43.235:8080/video')
video_capture = cv2.VideoCapture(0)
print("[INFO] i dont save this webcam session for output")
print("[INFO] load for gpu...sorry lah low gpu :( !!")
print("[INFO] harap bersabar....")

# Load a sample picture and learn how to recognize it.
faisal_image = face_recognition.load_image_file("dataset for facerec_from_webcam.py/Faisal.jpeg")
faisal_face_encoding = face_recognition.face_encodings(faisal_image)[0]

# Load a second sample picture and learn how to recognize it.
hazeq_image = face_recognition.load_image_file("dataset for facerec_from_webcam.py/Hazeq.jpg")
hazeq_face_encoding = face_recognition.face_encodings(hazeq_image)[0]

daus_image = face_recognition.load_image_file("dataset for facerec_from_webcam.py/Firdaus.jpg")
daus_face_encoding = face_recognition.face_encodings(daus_image)[0]

print("[INFO] starting video stream real quick...smileee")
# Create arrays of known face encodings and their names
known_face_encodings = [
    faisal_face_encoding,
   #playsound('/home/justnow/Desktop/face_recognition-master/commandPROJECT/music/music1.mp3');
    hazeq_face_encoding,
    daus_face_encoding
]
known_face_names = [
    "Faisal B031720043",
   "Hazeq B031810121",
    "Firdaus B031720002"
]


#if known_face_encoding = (faisal_face_encoding)
#print ("Faisal B031720043 hihih")


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown :("

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
	# 5 = thickness of frameline.
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 5)

        # Draw a label with a name below the face, 20=thickness of red frame
        cv2.rectangle(frame, (left, bottom - 20), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
	###name start at left bottom/top
	#(left + 5, bottom - 5) = dist from left is 5, dist from bottom is 5
        cv2.putText(frame, name, (left + 5, bottom - 5), font, 0.5, (255, 255, 255), 1)
	
	#eyes = eye_cascade.detectMultiScale( gray,     
        #scaleFactor=1.2,
       # minNeighbors=5,     
       # minSize=(20, 20))
	#for (ex,ey,ew,eh) in eyes:
	#   cv2.rectangle (roi_color, (ex, ey), (ex+ew,ey+eh), (0,255,0), 2)



    # Display the resulting image
    cv2.imshow('Detect face je ni', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()




