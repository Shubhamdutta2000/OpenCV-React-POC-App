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

video_resource = VideoCamera(active_captures, camera_index)

@app.post("/register_user/{USERNAME}")
async def register_user(USERNAME: str):
    global camera_status
    global camera_index
    global active_captures
    print(camera_status)
    
    if USERNAME not in camera_status:
        camera_status[USERNAME] = False
        active_captures[USERNAME] = None

        # check if camera index is in proper sequence or not 
        # and from 0 to len(camera_index) any number in sequence is missing 
        # or not then add that index to that username in camera_index
        for i in range(0, len(camera_index)):
            if i not in camera_index.values():
                camera_index[USERNAME] = i
                return {"message": "User registered successfully"}

        camera_index[USERNAME] = len(camera_status) - 1
    return {"message": "User registered successfully"}


@app.delete("/unregister_user/{USERNAME}")
async def unregister_user(USERNAME: str):
    camera_index.pop(USERNAME, "Username does not exist")
    camera_status.pop(USERNAME, "Username does not exist")
    active_captures.pop(USERNAME, "Username does not exist")
    return {"message": "User unregistered successfully"}


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
    camera_status[USERNAME] = True
    return StreamingResponse(gen(video_resource),
                             media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/camera_status/{USERNAME}")
async def camera_stat_route(USERNAME):
    # get username camera status
    return camera_status[USERNAME]


@app.delete("/stop/{USERNAME}")
async def stop_video(USERNAME: str):
    try:
        camera_status[USERNAME] = False
        # release video capture of specific user id
        video_resource.del_video(active_captures, USERNAME)
        return {"message": "Video resource released"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users")
async def get_user_list():
    print(camera_index)
    return list(camera_index.keys())



# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         # data = await websocket.receive_text()
#         await websocket.send_text(camera_index.keys())
