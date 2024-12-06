from fastapi import APIRouter, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import shutil
from backend.scan_engines import scan_with_virustotal

UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/upload")
async def upload_file(file: UploadFile):
    """Upload a file and scan it using VirusTotal."""
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        scan_result = scan_with_virustotal(file_path)
        if scan_result["status"] == "found":
            return {"message": "File scanned successfully.", "result": scan_result["result"]}
        elif scan_result["status"] == "uploaded":
            return {"message": "File submitted successfully.", "result": scan_result["result"]}
        else:
            return JSONResponse(content={"error": scan_result["message"]}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500) 