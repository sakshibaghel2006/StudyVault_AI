import json
import os

from document_processor import extract_pdf, extract_pptx
from chunker import create_chunks


# ==========================================
# FILE PATHS
# ==========================================

PDF_PATH = "data/documents/dbms.pdf"
PPT_PATH = "data/documents/DBMS_Presentation.pptx"

OCR_PATH = "data/processed/handwritten_ocr.json"

OUTPUT_PATH = "data/processed/chunks.json"


# ==========================================
# READ PDF
# ==========================================

print("Reading PDF...")

pdf_pages = extract_pdf(PDF_PATH)

print("PDF pages:", len(pdf_pages))


# ==========================================
# READ PPT
# ==========================================

print("Reading PowerPoint...")

ppt_slides = extract_pptx(PPT_PATH)

print("PPT slides:", len(ppt_slides))


# ==========================================
# CREATE PDF CHUNKS
# ==========================================

print("Creating PDF chunks...")

pdf_chunks = create_chunks(pdf_pages)

for chunk in pdf_chunks:
    chunk["source"] = "dbms.pdf"
    chunk["type"] = "pdf"


# ==========================================
# CREATE PPT CHUNKS
# ==========================================

print("Creating PPT chunks...")

ppt_chunks = create_chunks(ppt_slides)

for chunk in ppt_chunks:
    chunk["source"] = "DBMS_Presentation.pptx"
    chunk["type"] = "pptx"


# ==========================================
# READ HANDWRITTEN OCR
# ==========================================

print("Reading handwritten OCR...")

handwritten_chunks = []

if os.path.exists(OCR_PATH):

    with open(OCR_PATH, "r", encoding="utf-8") as file:
        ocr_data = json.load(file)

    for item in ocr_data:

        text = item.get("text", "").strip()

        if not text:
            continue

        handwritten_chunks.append({
            "text": text,
            "source": item.get("source", "handwritten_notes"),
            "type": "handwritten"
        })

    print("Handwritten pages:", len(handwritten_chunks))

else:

    print("Handwritten OCR file not found.")
    print("Expected:", OCR_PATH)


# ==========================================
# COMBINE ALL CHUNKS
# ==========================================

all_chunks = (
    pdf_chunks
    + ppt_chunks
    + handwritten_chunks
)


# ==========================================
# GIVE EVERY CHUNK A UNIQUE ID
# ==========================================

for index, chunk in enumerate(all_chunks, start=1):
    chunk["id"] = index


# ==========================================
# CREATE PROCESSED FOLDER
# ==========================================

os.makedirs("data/processed", exist_ok=True)


# ==========================================
# SAVE CHUNKS
# ==========================================

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        all_chunks,
        file,
        indent=2,
        ensure_ascii=False
    )


# ==========================================
# FINAL INFORMATION
# ==========================================

print("\n--- INGESTION COMPLETE ---")

print("PDF chunks:", len(pdf_chunks))
print("PPT chunks:", len(ppt_chunks))
print("Handwritten chunks:", len(handwritten_chunks))
print("Total chunks:", len(all_chunks))

print("\nSaved processed data to:")
print(OUTPUT_PATH)