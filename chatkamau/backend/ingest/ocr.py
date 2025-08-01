"""
text_extractor.py

This module provides functionality to extract text from PDF files using two OCR strategies:
1. EasyOCR
2. Kreuzberg's `extract_file` async utility

It chooses the result with the most text content and writes it to a specified output file.

Dependencies:
- easyocr
- kreuzberg (https://pypi.org/project/kreuzberg/)
- pdf2image
- numpy
- asyncio
- nest_asyncio

Usage Example:
--------------
from text_extractor import extract_best_text

await extract_best_text("/path/to/input.pdf", "/path/to/output.txt")
"""

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


# Example CLI usage or for testing:
if __name__ == "__main__":
    import sys

    # Accept paths as command line arguments or fallback to example
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "/content/AustinKimuhuNjugunaResume.pdf"
    out_txt = sys.argv[2] if len(sys.argv) > 2 else "/content/output.txt"

    asyncio.run(extract_best_text(pdf_path, out_txt))
