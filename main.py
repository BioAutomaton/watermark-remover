import cv2
from fastapi import FastAPI, UploadFile

from utils import image_from_bytes, zip_files, process_image

app = FastAPI()


@app.post("/")
async def unwatermark_image(files: list[UploadFile]):
    for index, uploaded_file in enumerate(files):
        try:
            contents = uploaded_file.file.read()  # read image bytes
            watermarked_image = image_from_bytes(contents)  # get cv2 image from bytes
            unwatermarked_image = process_image(watermarked_image)
            cv2.imwrite(f"{index}.jpg", unwatermarked_image)  # write image to disk
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            uploaded_file.file.close()

    return zip_files([f"{i}.jpg" for i in range(len(files))])
