import face_recognition
import cv2
import numpy as np
import time
# Load known faces
known_face_encodings = []
known_face_names = []

# Add known faces and names to the above lists

video_capture = cv2.VideoCapture(0)
# Load the face and eye cascade classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

lak_image = face_recognition.load_image_file("./train_dir/Himanshu/Himanshu.jpg")
lak_face_encoding = face_recognition.face_encodings(lak_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("./train_dir/Siddharth/Siddharth.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a second sample picture and learn how to recognize it.
mmsingh_image = face_recognition.load_image_file("./train_dir/mmsingh/Manmohan.JPG")
mmsingh_face_encoding = face_recognition.face_encodings(mmsingh_image)[0]


# Load a second sample picture and learn how to recognize it.
sat_image = face_recognition.load_image_file("./train_dir/Satinder/Satinder Kaur.JPG")
sat_face_encoding = face_recognition.face_encodings(sat_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    lak_face_encoding,
    biden_face_encoding,
    mmsingh_face_encoding,
    sat_face_encoding
]
known_face_names = [
    "Himanshu",
    "Pragya",
    "Manmohan",
    "Satinder"
]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # If no faces detected, display the original frame
    if len(faces) == 0:
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    for (x, y, w, h) in faces:
        # Extract the face ROI
        face_roi = frame[y:y+h, x:x+w]

        # Convert face ROI to grayscale
        face_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

        # Detect eyes in the grayscale face ROI
        eyes = eye_cascade.detectMultiScale(face_gray, 1.3, 5)

        # If no eyes or only one eye detected, display the original face ROI
        if len(eyes) == 0 or len(eyes) == 1:
            cv2.imshow('Video', face_roi)
            prev_time=0
            current_time = time.time()
            elapsed_time = current_time - prev_time
            prev_time = current_time

            # Calculate bandwidth of the current frame
            bandwidth = len(face_roi.tobytes()) / elapsed_time

            # Print the bandwidth
            print("Face_bandwidth:", bandwidth)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        # Extract the first two eye ROIs
        eye1 = eyes[0]
        eye2 = eyes[1]

        # Determine the x, y, width, and height of the bounding box
        # containing both eye ROIs, with a gap of 10 pixels between them
        x = min(eye1[0], eye2[0]) - 10
        y = min(eye1[1], eye2[1]) - 10
        w = max(eye1[0] + eye1[2], eye2[0] + eye2[2]) - x + 10
        h = max(eye1[1] + eye1[3], eye2[1] + eye2[3]) - y + 10

        # Extract the combined eye ROIs from the face ROI
        eyes_roi = face_roi[y:y+h, x:x+w]

        # Display the combined eye ROIs
        cv2.imshow('Video', eyes_roi)
        prev_time=0
        current_time = time.time()
        elapsed_time = current_time - prev_time
        prev_time = current_time

        # Calculate bandwidth of the current frame
        bandwidth = len(eyes_roi.tobytes()) / elapsed_time

        # Print the bandwidth
        print("Extracted_Eyes_bandwidth:", bandwidth)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

