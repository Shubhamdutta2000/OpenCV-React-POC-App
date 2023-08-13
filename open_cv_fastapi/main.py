from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.responses import StreamingResponse
from camera import VideoCamera

app = FastAPI()

# class SimpleVideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#     def __del__(self):
#         self.video.release()
#     def get_frame(self):
#         ret, frame = self.video.read()
#         ret, jpeg = cv2.imencode('.jpg', frame)
#         return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.get("/")
def read_root(request: Request):
    return {
        "message": "Hello User 🙏"
    }

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(gen(VideoCamera()),
                             media_type='multipart/x-mixed-replace; boundary=frame')

