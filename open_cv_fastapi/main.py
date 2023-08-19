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

# Maintain camera status for each user
camera_status = {}

# Maintain camera index for each user
camera_index = {}

# Maintain active video captures for each user
active_captures = {}

@app.post("/register_user/{USERNAME}")
async def register_user(USERNAME: str):
    global camera_status
    global camera_index
    global active_captures
    
    if USERNAME not in camera_status:
        camera_status[USERNAME] = False
        camera_index[USERNAME] = len(camera_status) - 1
        active_captures[USERNAME] = None
        
    return {"message": "User registered successfully"}


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

@app.get("/video_feed/{USERNAME}")
async def video_feed(USERNAME: str):
    # get frame of specific video capture based on specific camera index and user_id
    video_resource = VideoCamera(active_captures, camera_index, USERNAME)
    return StreamingResponse(gen(video_resource),
                             media_type='multipart/x-mixed-replace; boundary=frame')


@app.delete("/stop/{USERNAME}")
async def stop_video(USERNAME: str):
    try:
        # release video capture of specific user id
        video_resource.__del__(active_captures, USERNAME)
        return {"message": "Video resource released"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users")
async def get_user_list():
    print(camera_index)
    return list(camera_index.keys())
