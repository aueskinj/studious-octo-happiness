import os
import json
from pdf2image import convert_from_path
from PIL import Image, ImageDraw

import easyocr
import numpy as np
import torch
from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification

# """## Convert PDF to images"""

# from pdf2image import convert_from_path
# import os

# # Convert PDF to images
# images = convert_from_path("/content/Austin_Njuguna.pdf", dpi=300)
# image_paths = []

# for i, page in enumerate(images):
#     image_path = f"page_{i+1}.png"
#     page.save(image_path, "PNG")
#     image_paths.append(image_path)

# """## Use easy OCR"""

# import easyocr
# import matplotlib.pyplot as plt
# from PIL import Image

# reader = easyocr.Reader(['en'])  # You can add other languages

# for image_path in image_paths:
#     result = reader.readtext(image_path, detail=1)  # detail=1 gives bounding boxes

#     # Visualize
#     img = Image.open(image_path)
#     plt.imshow(img)
#     for detection in result:
#         bbox, text, conf = detection
#         print(f"[EASYOCR] Text: {text}, Confidence: {conf}")

# """## Postprocess OCR Output"""

# import json
# import numpy as np # Import numpy to check for int32 type

# output = []
# for image_path in image_paths:
#     result = reader.readtext(image_path, detail=1)
#     for box, text, conf in result:
#         # Convert numpy int32 to standard int for JSON serialization
#         bbox_list = [[int(coord) for coord in point] for point in box]
#         output.append({
#             "image": image_path,
#             "text": text,
#             "confidence": float(conf), # Ensure confidence is a standard float
#             "bbox": bbox_list
#         })

# with open("easyocr_output.json", "w") as f:
#     json.dump(output, f, indent=2)

# """## Model Pipeline"""



# OCR Reader
reader = easyocr.Reader(['en'])

# LayoutLMv3 processor + model
processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=False)
model = LayoutLMv3ForTokenClassification.from_pretrained("microsoft/layoutlmv3-base")

def normalize_bbox(bbox, width, height):
    return [
        int(1000 * bbox[0] / width),
        int(1000 * bbox[1] / height),
        int(1000 * bbox[2] / width),
        int(1000 * bbox[3] / height),
    ]

def process_pdf(pdf_path, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=300)

    summary = []

    for idx, img in enumerate(images):
        image_path = os.path.join(output_dir, f"page_{idx+1}.png")
        img.save(image_path)
        print(f"[INFO] Processing {image_path}...")

        width, height = img.size
        ocr_result = reader.readtext(image_path, detail=1)

        # Preprocess OCR results for token classification
        words = [str(text) for box, text, conf in ocr_result]
        boxes = [normalize_bbox((box[0][0], box[0][1], box[2][0], box[2][1]), width, height)
                 for box, _, _ in ocr_result]

        encoding = processor(
            images=[img],
            text=[words],
            boxes=[boxes],
            return_tensors="pt",
            truncation=True,
            padding="max_length"
        )

        with torch.no_grad():
            outputs = model(**encoding)

        predictions = torch.argmax(outputs.logits, dim=2)
        label_ids = predictions[0].tolist()

        layout_results = []
        for word, box, label_id in zip(words, boxes, label_ids):
            layout_results.append({
                "word": word,
                "bbox": [int(c) for c in box],
                "label": model.config.id2label[label_id]
            })

        # Draw annotations for table tokens
        draw = ImageDraw.Draw(img)
        for item in layout_results:
            if "table" in item["label"].lower():
                x0, y0, x1, y1 = [int(val * width / 1000) for val in item["bbox"]]
                draw.rectangle([x0, y0, x1, y1], outline="red", width=2)

        # EasyOCR raw output, JSON-safe
        easyocr_output = []
        for box, text, conf in ocr_result:
            bbox_list = [[int(coord) for coord in point] for point in box]
            easyocr_output.append({
                "bbox": bbox_list,
                "text": str(text),
                "confidence": float(conf)
            })

        # Grouping logic: glossary-like key-value pairing
        glossary_pairs = []
        used_indices = set()
        for i, item in enumerate(layout_results):
            if i in used_indices or len(item["word"].split()) > 4:
                continue
            curr_y = item["bbox"][1]
            min_dist = float("inf")
            best_match = None

            for j in range(i + 1, len(layout_results)):
                next_item = layout_results[j]
                if j in used_indices:
                    continue
                next_y = next_item["bbox"][1]
                dist = next_y - curr_y
                if 10 < dist < 80 and len(next_item["word"].split()) > 4:
                    if dist < min_dist:
                        best_match = (j, next_item)
                        min_dist = dist

            if best_match:
                glossary_pairs.append({
                    "term": item["word"],
                    "definition": best_match[1]["word"]
                })
                used_indices.update([i, best_match[0]])

        # Table grouping based on y-coordinate clustering
        def cluster_table_rows(tokens, y_thresh=20):
            rows = []
            sorted_tokens = sorted(tokens, key=lambda x: x["bbox"][1])
            current_row = []

            for token in sorted_tokens:
                if not current_row:
                    current_row.append(token)
                    continue
                y_diff = abs(token["bbox"][1] - current_row[-1]["bbox"][1])
                if y_diff <= y_thresh:
                    current_row.append(token)
                else:
                    rows.append(current_row)
                    current_row = [token]
            if current_row:
                rows.append(current_row)
            return rows

        table_tokens = [t for t in layout_results if "table" in t["label"].lower()]
        table_rows = cluster_table_rows(table_tokens)

        page_output = {
            "image": image_path,
            "layoutlmv3_results": layout_results,
            "raw_easyocr": easyocr_output,
            "glossary_pairs": glossary_pairs,
            "detected_table_rows": [
                [{"text": cell["word"], "bbox": cell["bbox"]} for cell in row]
                for row in table_rows
            ]
        }

        # Save annotated image
        img.save(os.path.join(output_dir, f"page_{idx+1}_annotated.png"))
        summary.append(page_output)

    # Save structured JSON
    with open(os.path.join(output_dir, "layoutlmv3_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print(f"[DONE] Results saved to {output_dir}")

# process_pdf('/content/Austin_Njuguna.pdf')
# process_pdf('/content/Basics.pdf')