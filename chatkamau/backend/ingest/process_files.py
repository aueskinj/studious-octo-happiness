import os
import asyncio
from pathlib import Path
import numpy as np
from kreuzberg import extract_file  # async
from easyocr import Reader
from pdf2image import convert_from_path
import nest_asyncio

nest_asyncio.apply()

def easyocr_extract(pdf_path, languages=["en"]):
    """
    Extract text from a PDF using EasyOCR.

    Args:
        pdf_path (str): Path to the PDF file.
        languages (list[str]): List of languages (e.g., ['en']).

    Returns:
        str: Extracted text as a single string.
    """
    reader = Reader(languages, gpu=False)
    pages = convert_from_path(pdf_path)
    texts = []
    for page in pages:
        result = reader.readtext(np.array(page), detail=0)
        texts.append("\n".join(result))
    return "\n\n".join(texts)

async def kreuzberg_extract(pdf_path):
    """
    Extract text from a PDF using Kreuzberg's async extractor.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text as a single string.
    """
    result = await extract_file(pdf_path)
    return result.content or ""

async def extract_best_text(pdf_path: str, out_txt: str):
    """
    Run multiple OCR methods and save the result with the longest content.

    Args:
        pdf_path (str): Path to the input PDF file.
        out_txt (str): Path to save the extracted text.

    Returns:
        None
    """
    out_path = Path(out_txt)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Run both extractors in parallel
    kb_task = kreuzberg_extract(pdf_path)
    loop = asyncio.get_event_loop()
    ez_task = loop.run_in_executor(None, easyocr_extract, pdf_path)

    kb, ez = await asyncio.gather(kb_task, ez_task)

    candidates = [("kreuzberg", kb), ("easyocr", ez)]
    label, content = max(candidates, key=lambda pair: len(pair[1] or ""))

    print(f"Selected extractor: {label} (text length: {len(content)})")
    out_path.write_text(content, encoding="utf-8")
    print(f"Wrote extracted text to {out_txt}")

async def process_uploaded_files(file_paths: list[str]):
    """
    Processes a batch of uploaded files.

    Args:
        file_paths (list[str]): A list of paths to the uploaded files.
    """
    print("Starting batch processing of uploaded files...")

    for file_path in file_paths:
        if file_path.lower().endswith('.pdf'):
            try:
                output_txt_path = os.path.splitext(file_path)[0] + '.txt'
                await extract_best_text(file_path, output_txt_path)
                print(f"Processed PDF file: {file_path}")
            except Exception as e:
                print(f"Error processing PDF file {file_path}: {e}")
        else:
            print(f"Skipping unsupported file type: {file_path}")

    print("Batch processing complete.")