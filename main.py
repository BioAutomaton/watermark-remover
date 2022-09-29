import base64

import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')


def load_image_into_numpy_array(data):
    npimg = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    return frame


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/uploadfiles/")
async def create_upload_files(request: Request, files: list[UploadFile]):
    for file in files:
        try:
            contents = file.file.read()
            image = load_image_into_numpy_array(contents)
            _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
            cv2.imwrite("image.jpg", thresh)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()

    return FileResponse('image.jpg')

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})
