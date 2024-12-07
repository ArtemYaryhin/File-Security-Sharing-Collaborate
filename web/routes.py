from fastapi import APIRouter, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import shutil
from backend.scan_engines import scan_with_virustotal, scan_with_hybrid_analysis

UPLOAD_FOLDER = "uploaded_files"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
router = APIRouter()
templates = Jinja2Templates(directory="web/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/upload")
async def upload_file(file: UploadFile, engine: str = Form("vt")):
    """Upload a file and scan it using VirusTotal or Hybrid Analysis."""

    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if engine == "vt":
            scan_result = await scan_with_virustotal(file_path)
        elif engine == "ha":
            scan_result = await scan_with_hybrid_analysis(file_path)
        else:
            return JSONResponse(content={"error": "Unsupported engine. Use 'vt' or 'ha'."}, status_code=400)

        if scan_result["status"] == "found":
            return templates.TemplateResponse("index.html", {
                "request": Request,
                "message": "File scanned successfully.",
                "result": scan_result["result"]
            })
        elif scan_result["status"] == "uploaded":
            return templates.TemplateResponse("index.html", {
                "request": Request,
                "message": "File submitted successfully.",
                "result": scan_result["result"]
            })
        else:
            return templates.TemplateResponse("index.html", {
                "request": Request,
                "error": scan_result["message"]
            })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": Request,
            "error": str(e)
        }) 
