import os
import asyncio
from ocr import extract_best_text

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

if __name__ == '__main__':
    # Example usage (for testing the function directly)
    # Replace with actual file paths for testing
    dummy_files = ["./test_docs/document1.pdf", "./test_docs/image.jpg", "./test_docs/document2.pdf"]
    asyncio.run(process_uploaded_files(dummy_files))