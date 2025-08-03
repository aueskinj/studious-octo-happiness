### `/backend/ingest`

Document and data ingestion tools. The `__init__.py` file in this directory orchestrates the ingestion process.

* `reader.py`: Handle text, PDF, DOCX, XLSX, CSV
* `text_extractor.py`: Provides OCR functionality for extracting text from PDF files using multiple strategies (EasyOCR, Kreuzberg).
* `process_files.py`: Contains the logic for processing uploaded files, utilizing `text_extractor.py` for PDF files.
* `audio_transcribe.py`: Transcribe audio (Whisper-tiny/Vosk)
* `chunker.py`: Break down text for embedding
