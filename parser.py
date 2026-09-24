"""
Document parsing module for SkillGap.
Uses pdfplumber to reliably extract clean text from multi-page PDF resumes.
"""

import io
from typing import Union
import pdfplumber


def extract_text_from_pdf(pdf_source: Union[bytes, io.BytesIO, any]) -> str:
    """
    Extract readable text from a PDF file using pdfplumber.
    Accepts bytes, file-like object, or Streamlit UploadedFile.
    """
    extracted_text = []

    if hasattr(pdf_source, "read"):
        file_bytes = pdf_source.read()
        if hasattr(pdf_source, "seek"):
            pdf_source.seek(0)
        pdf_file = io.BytesIO(file_bytes)
    elif isinstance(pdf_source, (bytes, bytearray)):
        pdf_file = io.BytesIO(pdf_source)
    else:
        pdf_file = pdf_source

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

    return "\n\n".join(extracted_text).strip()
