import io
import os
import zipfile

import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, Request, Response
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')


def load_image_into_numpy_array(data):
    npimg = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    return frame


def zipfiles(filenames: list):
    zip_filename = "archive.zip"

    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)

        # Add file, at correct path
        zf.write(fpath, fname)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })

    return resp


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


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
