import cv2
import time


class VideoCamera(object):
    def __init__(self, active_captures, camera_index, user_id=None):
        # Check if any active video capture present or not otherwise create a video capture 
        # based on the corresponding camera index and user_id
        print("active_captures", active_captures)
        if user_id is not None:
            if active_captures.get(user_id) is None:
                self.video = cv2.VideoCapture(camera_index[user_id])
                active_captures[user_id] = self.video
            else:
                self.video = active_captures[user_id]

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml')

    def del_video(self, active_captures, user_id):
         # release active video capure of specific user id 
         self.video = active_captures.pop(user_id, None)
         if self.video:
            self.video.release()

    def get_frame(self):
        last_eye_detection_time = time.time()
        current_time = time.time()
        prev_time = current_time
        while True:
            ret, frame = self.video.read()
            if not ret:
                break

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            current_time = time.time()
            # Detect faces in the grayscale frame
            
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(70, 70))

            eyes_detected = False

            for (x, y, w, h) in faces:
                # Extract the face ROI
                face_roi = gray[y:y+h, x:x+w]

                # Detect eyes in the grayscale face ROI
                eyes = self.eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

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
                    print(last_eye_detection_time,"last_eye_detection")
                    
                    eyes_detected = True

            # If eyes were not detected for 10 seconds, display the complete video
            if not eyes_detected and (time.time() - last_eye_detection_time > 10):
        
                # Calculate bandwidth for the entire frame
                current_time = time.time()
                elapsed_time = current_time - prev_time
                frame_bandwidth = len(frame.tobytes()) / elapsed_time
                print("Frame_bandwidth:", frame_bandwidth, "bytes/second")

                ret, jpeg = cv2.imencode('.jpg', frame)
                return jpeg.tobytes()

            elif eyes_detected:
                # Calculate bandwidth for the extracted eyes
                current_time = time.time()
                elapsed_time = current_time - prev_time
                eye_bandwidth = len(extracted_eyes.tobytes()) / elapsed_time
                print("Extracted_Eyes_bandwidth:", eye_bandwidth, "bytes/second")

                ret, jpeg = cv2.imencode('.jpg', extracted_eyes)
                return jpeg.tobytes()

            prev_time = current_time
                        # Print the bandwidth
                        # print("Extracted_Eyes_bandwidth:", bandwidth)
                        # ret, jpeg = cv2.imencode('.jpg', eyes_roi)
                        # return jpeg.tobytes()
                        # if cv2.waitKey(1) & 0xFF == ord('q'):
                        #     break
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
