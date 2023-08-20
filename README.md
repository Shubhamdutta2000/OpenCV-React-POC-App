# OpenCV-React-POC-App

- Integrating your opencv project into a react component using fastapi
- This repository contains a project that demonstrates how to build an image processing application using OpenCV, with FastAPI as the backend framework and Node.js with EJS as the frontend framework.
- The application allows users to upload images, apply various image processing techniques, and view the processed images.

## Features

- Create Instant meet: Users can create instant meet and multiple user in a same local server can join the meet.
- Image processing: The uploaded images can be processed using OpenCV image processing techniques like face and eye detection.
- Real-time preview: Users can see the preview of the processed image on the frontend.
- Start the meeting using the button provided.
- The meeting can be run locally only.
- Use two webcameras one in chrome and the other one in incognito.
- The same URL must be opened in the incognito window.
- The video feed will get displayed along with the processing of the video.(the openCV code for eye detection)
- The video feed can be turned on/off.
- User can leave from a specific meeting 
  
##  Prerequisites

- Before you begin, ensure you have met the following requirements:

  - Install Python 3.x and Node.js on your system.
  - Install the required Python packages by running pip install -r requirements.txt.
  - Install the required Node.js packages by running npm install in the frontend directory.



## Getting Started

- Clone this repository:

```
git clone https://github.com/your-username/opencv-fastapi-nodeejs.git
```

- Navigate to the project directory:

```
cd open_cv_fastapi

# for first time to create virtual environment
python -m venv venv

# to activate virtual env (required every time)
source venv/Scripts/activate
```

- Start the FastAPI backend:

```
uvicorn main:app --reload
```

The backend will run at http://127.0.0.1:8000.

- Start the Node.js frontend:

```
cd videoconf_frontend
npm i
npm start
```

The frontend will be accessible at http://localhost:5000.

## Contributing

- Contributions are welcome! If you find any issues or want to enhance the project, feel free to submit a pull request.

## Blog to folow:

- https://medium.com/@jadomene99/integrating-your-opencv-project-into-a-react-component-using-flask-6bcf909c07f4
