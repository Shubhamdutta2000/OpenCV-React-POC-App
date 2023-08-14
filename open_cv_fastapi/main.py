from fastapi import FastAPI, Request, Response, BackgroundTasks,HTTPException
from fastapi.responses import StreamingResponse
from camera import VideoCamera
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
global video_resource
video_resource = VideoCamera()
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
    video_resource = VideoCamera()
    return StreamingResponse(gen(video_resource),
                             media_type='multipart/x-mixed-replace; boundary=frame')


@app.delete("/stop")
async def stop_video():
    
    try:
        video_resource.__del__()
        return {"message": "Video resource released"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))