import os
import re
import sqlite3
from PIL import Image
import pytesseract

# --- CONFIGURATION ---
IMAGE_FOLDER = "C:\\kronika\\images"
OCR_OUTPUT_FOLDER = "C:\\kronika\\ocr_output"
DB_FILE = "C:\\kronika\\database\\book_index.db"

# If Tesseract is not in your PATH, point to it manually:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- HELPER FUNCTIONS ---

def init_db(db_file):
    """Create SQLite table if it doesn’t exist."""
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_number INTEGER,
            filename TEXT,
            paragraph TEXT
        )
    """)
    conn.commit()
    return conn

def clean_text(text):
    """Normalize whitespace and remove non-printables."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def ocr_image(image_path):
    """Run OCR on one image and return extracted text."""
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img, lang="eng")
    return text

def process_images(image_folder, ocr_output_folder, conn):
    """Scan images, OCR them, and store in DB."""
    os.makedirs(ocr_output_folder, exist_ok=True)
    cur = conn.cursor()

    images = sorted(
        [f for f in os.listdir(image_folder) if f.lower().endswith((".jpg", ".png"))]
    )

    for idx, filename in enumerate(images, start=1):
        page_path = os.path.join(image_folder, filename)
        print(f"Processing page {idx}/{len(images)}: {filename}")

        # OCR step
        text = ocr_image(page_path)
        if not text.strip():
            print(f"⚠️  No text found in {filename}")
            continue

        # Save OCR text to .txt for manual reference
        out_txt = os.path.join(ocr_output_folder, os.path.splitext(filename)[0] + ".txt")
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(text)

        # Split into paragraphs (double newline or long single lines)
        paragraphs = [clean_text(p) for p in re.split(r"\n\s*\n", text) if p.strip()]

        # Insert into DB
        for para in paragraphs:
            cur.execute(
                "INSERT INTO pages (page_number, filename, paragraph) VALUES (?, ?, ?)",
                (idx, filename, para),
            )
        conn.commit()

    print("✅ OCR and indexing complete.")

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    conn = init_db(DB_FILE)
    process_images(IMAGE_FOLDER, OCR_OUTPUT_FOLDER, conn)
    conn.close()
