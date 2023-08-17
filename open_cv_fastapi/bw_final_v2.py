#import face_recognition
import cv2
import numpy as np
import time

video_capture = cv2.VideoCapture(0)

# Load the face and eye cascade classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

prev_time = time.time()
last_eye_detection_time = time.time()

while True:
    ret, frame = video_capture.read()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Get the current time at the start of each iteration.
    current_time = time.time()


    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(70, 70))

    eyes_detected = False

    for (x, y, w, h) in faces:
        # Extract the face ROI
        face_roi = gray[y:y+h, x:x+w]

        # Detect eyes in the grayscale face ROI
        eyes = eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Extract both eyes together
        if len(eyes) == 2:
            sorted_eyes = sorted(eyes, key=lambda eye: eye[0])

            ex1, ey1, ew1, eh1 = sorted_eyes[0]
            ex2, ey2, ew2, eh2 = sorted_eyes[1]

            eye_x = min(ex1, ex2)
            eye_y = min(ey1, ey2)
            eye_w = max(ex1 + ew1, ex2 + ew2) - eye_x
            eye_h = max(ey1 + eh1, ey2 + eh2) - eye_y

            extracted_eyes = face_roi[eye_y:eye_y+eye_h, eye_x:eye_x+eye_w]

            # Update the last time eyes were detected
            last_eye_detection_time = time.time()
            
            eyes_detected = True

    # If eyes were not detected for 10 seconds, display the complete video
    if not eyes_detected and (time.time() - last_eye_detection_time > 10):
        cv2.imshow('Video', frame)

        # Calculate bandwidth for the entire frame
        current_time = time.time()
        elapsed_time = current_time - prev_time
        frame_bandwidth = len(frame.tobytes()) / elapsed_time
        print("Frame_bandwidth:", frame_bandwidth, "bytes/second")

    elif eyes_detected:
        cv2.imshow('Video', extracted_eyes)

        # Calculate bandwidth for the extracted eyes
        current_time = time.time()
        elapsed_time = current_time - prev_time
        eye_bandwidth = len(extracted_eyes.tobytes()) / elapsed_time
        print("Extracted_Eyes_bandwidth:", eye_bandwidth, "bytes/second")

    prev_time = current_time

    # Quit the program if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
