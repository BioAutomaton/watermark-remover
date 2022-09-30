import cv2
from fastapi import FastAPI, UploadFile, Request
from fastapi.templating import Jinja2Templates

from utils import load_image_into_numpy_array, zipfiles

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.post("/uploadfiles/")
async def create_upload_files(request: Request, files: list[UploadFile]):
    for i, file in enumerate(files):
        try:
            contents = file.file.read()
            image = load_image_into_numpy_array(contents)
            _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
            cv2.imwrite(f"{i}.jpg", thresh)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()

    return zipfiles([f"{i}.jpg" for i in range(len(files))])


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})
