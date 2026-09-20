import os
from PIL import Image
import pytesseract
from pypdf import PdfReader

# ----------------------------
# Tesseract Path (Windows)
# ----------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ----------------------------
# Read Text From Image
# ----------------------------
def read_image(image_path):

    try:

        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        return text

    except Exception as e:

        return f"OCR Error: {e}"


# ----------------------------
# Read Text From PDF
# ----------------------------
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


# ----------------------------
# Detect File Type
# ----------------------------
def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    elif extension in [".png", ".jpg", ".jpeg"]:
        return read_image(file_path)

    else:
        return "Unsupported file type."