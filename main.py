import base64

from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/uploadfiles/")
async def create_upload_files(request: Request, files: list[UploadFile]):
    for file in files:
        try:
            contents = file.file.read()
            with open("uploaded_" + file.filename, "wb") as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()

    base64_encoded_image = base64.b64encode(contents).decode("utf-8")

    return templates.TemplateResponse("display.html", {"request": request, "myImage": base64_encoded_image})


@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
