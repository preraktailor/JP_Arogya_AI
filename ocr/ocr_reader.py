import os
from PIL import Image
import pytesseract
from pypdf import PdfReader

# Tesseract configuration
# Windows: use installed Tesseract path
# Linux/Render: use system "tesseract" command

if os.name == "nt":
    windows_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(windows_tesseract):
        pytesseract.pytesseract.tesseract_cmd = windows_tesseract


def read_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"OCR Error: {e}"


def read_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    except Exception as e:
        return f"PDF Error: {e}"


def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    elif extension in [".png", ".jpg", ".jpeg"]:
        return read_image(file_path)

    else:
        return "Unsupported file type."

