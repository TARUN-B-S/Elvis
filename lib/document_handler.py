from pdf2image import convert_from_path
import pytesseract
import os
import subprocess

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path, dpi=200)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def convert_docx_to_pdf(docx_path):
    pdf_path = docx_path.replace(".pdf", ".pdf")
    pdf_path = docx_path.replace(".docx", ".pdf")
    pdf_path = docx_path.replace(".odt", ".pdf")  # Handle .odt files as well
    pdf_path = docx_path.replace(".doc", ".pdf")  # Handle .doc files as well
    pdf_path = docx_path.replace(".ppt", ".pdf")  # Handle .ppt files as well
    pdf_path = docx_path.replace(".pptx", ".pdf")  # Handle .pptx files as well
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(pdf_path), docx_path])
    return pdf_path
