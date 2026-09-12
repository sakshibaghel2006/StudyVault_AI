from document_processor import extract_pdf, extract_pptx
from chunker import create_chunks


# ==========================================
# FILE PATHS
# ==========================================

pdf_path = "data/documents/dbms.pdf"
ppt_path = "data/documents/DBMS_Presentation.pptx"


# ==========================================
# EXTRACT PDF AND PPT TEXT
# ==========================================

pdf_pages = extract_pdf(pdf_path)
ppt_slides = extract_pptx(ppt_path)


# ==========================================
# DOCUMENT COUNTS
# ==========================================

print("PDF pages:", len(pdf_pages))
print("PPT slides:", len(ppt_slides))


# ==========================================
# PDF PAGE 1
# ==========================================

print("\n--- PDF PAGE 1 ---")

pdf_text = pdf_pages[0]["text"]

# Change department name only in terminal output
pdf_text = (
    pdf_text
    .replace("CS Dept.", "IT Dept.")
    .replace("CS Department", "IT Department")
)

print(pdf_text[:500])


# ==========================================
# PPT SLIDE 1
# ==========================================

print("\n--- PPT SLIDE 1 ---")

ppt_text = ppt_slides[0]["text"]

# Change department name only in terminal output
ppt_text = (
    ppt_text
    .replace("CS Dept.", "IT Dept.")
    .replace("CS Department", "IT Department")
)

print(ppt_text[:500])


# ==========================================
# CREATE PDF CHUNKS
# ==========================================

pdf_chunks = create_chunks(pdf_pages)


# ==========================================
# CHUNK TEST
# ==========================================

print("\n--- CHUNK TEST ---")

print("Total chunks:", len(pdf_chunks))

print("First chunk page:", pdf_chunks[0]["page"])

print("First chunk text:")

chunk_text = pdf_chunks[0]["text"]

# Change department name only in terminal output
chunk_text = (
    chunk_text
    .replace("CS Dept.", "IT Dept.")
    .replace("CS Department", "IT Department")
)

print(chunk_text[:300])