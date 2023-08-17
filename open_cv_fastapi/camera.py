import cv2
import time


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml')

    def __del__(self):
        self.video.release()

    def get_frame(self):

        while True:
            ret, frame = self.video.read()
            if not ret:
                break

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the grayscale frame
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            # If no faces detected, display the original frame
            if len(faces) == 0:
                # cv2.imshow('Video', frame)
                ret, jpeg = cv2.imencode('.jpg', frame)
                return jpeg.tobytes()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue

            for (x, y, w, h) in faces:
                # Extract the face ROI
                face_roi = frame[y:y+h, x:x+w]

                # Convert face ROI to grayscale
                face_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

                # Detect eyes in the grayscale face ROI
                eyes = self.eye_cascade.detectMultiScale(face_gray, 1.3, 5)

                # If no eyes or only one eye detected, display the original face ROI
                if len(eyes) == 0 or len(eyes) == 1:
                    # cv2.imshow('Video', face_roi)

                    prev_time = 0
                    current_time = time.time()
                    elapsed_time = current_time - prev_time
                    prev_time = current_time

                    # Calculate bandwidth of the current frame
                    bandwidth = len(face_roi.tobytes()) / elapsed_time

                    # Print the bandwidth
                    print("Face_bandwidth:", bandwidth)

                    # if cv2.waitKey(1) & 0xFF == ord('q'):
                    #     break

                    ret, jpeg = cv2.imencode('.jpg', face_roi)
                    return jpeg.tobytes()

                    # continue

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
                # cv2.imshow('Video', eyes_roi)

                prev_time = 0
                current_time = time.time()
                elapsed_time = current_time - prev_time
                prev_time = current_time

                # Calculate bandwidth of the current frame
                bandwidth = len(eyes_roi.tobytes()) / elapsed_time

                # Print the bandwidth
                print("Extracted_Eyes_bandwidth:", bandwidth)
                ret, jpeg = cv2.imencode('.jpg', eyes_roi)
                return jpeg.tobytes()
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

            time.sleep(1000)
        # ret, frame = self.video.read()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # # Detect faces
        # faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        # # Draw rectangle around faces and detect eyes inside them
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #     roi_gray = gray[y:y + h, x:x + w]
        #     roi_color = frame[y:y + h, x:x + w]
        #     eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 3)

        #     # Draw rectangle around eyes
        #     for (ex, ey, ew, eh) in eyes:
        #         cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        # ret, jpeg = cv2.imencode('.jpg', frame)
        # return jpeg.tobytes()
