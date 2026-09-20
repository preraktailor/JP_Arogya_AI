import os
import shutil

from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ocr.ocr_reader import extract_text
from utils.ai_model import analyze_report
from database.db import save_report

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# -----------------------------------
# Upload Page
# -----------------------------------
@router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):

    if "user" not in request.session:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={
            "request": request,
            "user": request.session["user"]
        }
    )


# -----------------------------------
# Upload Report
# -----------------------------------
@router.post("/upload", response_class=HTMLResponse)
async def upload_report(
    request: Request,
    report: UploadFile = File(...)
):

    if "user" not in request.session:
        return RedirectResponse(url="/login", status_code=303)

    # Create uploads folder
    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", report.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(report.file, buffer)

    # OCR
    report_text = extract_text(file_path)
    print("✅ OCR Done")

    # AI Analysis
    result = analyze_report(report_text)
    print("✅ AI Done")

    # Save Report
    print("Saving Report...")

    save_report(
        request.session["user"]["email"],
        report.filename,
        report_text,
        result
    )

    print("✅ Report Saved Successfully")

    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context={
            "request": request,
            "user": request.session["user"],
            "filename": report.filename,
            "result": result
        }
    )