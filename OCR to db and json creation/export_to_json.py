import sqlite3
import json

DB_PATH = "database/book_index.db"
OUTPUT_JSON = "web/book_data.json"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT page_number, filename, paragraph FROM pages")
rows = cur.fetchall()

data = []
for page_number, filename, paragraph in rows:
    data.append({
        "page": page_number,
        "filename": filename,
        "paragraph": paragraph
    })

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Exported {len(data)} paragraphs to {OUTPUT_JSON}")
