import os
import json
from pathlib import Path

import pytesseract
from PIL import Image


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
else:
    print("WARNING: Tesseract executable not found at:")
    print(TESSERACT_PATH)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

HANDWRITTEN_DIR = BASE_DIR / "data" / "documents" / "handwritten"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_FILE = OUTPUT_DIR / "handwritten_ocr.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# OCR FUNCTION
# ============================================================

def extract_text_from_image(image_path):
    """
    Extract text from a handwritten/scanned image using Tesseract OCR.
    """

    try:
        image = Image.open(image_path)

        # Convert image to RGB for reliable OCR processing
        image = image.convert("RGB")

        # OCR configuration
        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        return text.strip()

    except Exception as e:
        raise RuntimeError(str(e))


# ============================================================
# PROCESS ALL HANDWRITTEN IMAGES
# ============================================================

def process_handwritten_images():

    print("=" * 45)
    print("          STUDYVAULT AI - OCR")
    print("=" * 45)

    # Check Tesseract
    try:
        version = pytesseract.get_tesseract_version()
        print(f"\nTesseract detected: {version}")
    except Exception as e:
        print("\nERROR: Tesseract could not be detected.")
        print(e)
        return

    # Check handwritten folder
    if not HANDWRITTEN_DIR.exists():
        print("\nHandwritten folder not found:")
        print(HANDWRITTEN_DIR)
        return

    # Find supported image files
    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tiff",
        ".tif",
        ".webp"
    }

    image_files = [
        file for file in HANDWRITTEN_DIR.iterdir()
        if file.is_file() and file.suffix.lower() in image_extensions
    ]

    print(f"\nImages found: {len(image_files)}")

    if not image_files:
        print("No handwritten images found.")
        return

    results = []

    # Process each image
    for index, image_path in enumerate(image_files, start=1):

        print(f"\nProcessing {index}: {image_path.name}")

        result = {
            "source": image_path.name,
            "type": "handwritten",
            "text": ""
        }

        try:

            extracted_text = extract_text_from_image(image_path)

            result["text"] = extracted_text

            print("OCR successful.")
            print(f"Characters extracted: {len(extracted_text)}")

        except Exception as e:

            result["error"] = str(e)

            print("OCR failed:")
            print(e)

        results.append(result)

    # ========================================================
    # SAVE OCR RESULTS
    # ========================================================

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 45)
    print("        OCR PROCESSING COMPLETE")
    print("=" * 45)

    print(f"\nImages processed: {len(results)}")

    print("\nSaved OCR data to:")
    print(OUTPUT_FILE)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    process_handwritten_images()