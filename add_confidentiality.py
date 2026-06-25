# add_confidentiality.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")

# Проверяем, есть ли уже такое соглашение
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(
    "SELECT id FROM documents WHERE title = 'Соглашение о конфиденциальности' AND doc_type = 'Соглашение о конфиденциальности'"
)
if cursor.fetchone() is None:
    cursor.execute(
        "INSERT INTO documents (title, doc_type, file_url, date) VALUES (?, ?, ?, ?)",
        ("Соглашение о конфиденциальности", "Соглашение о конфиденциальности", "/static/docs/confidentiality_agreement.docx", "2025-11-25")
    )
    print("✅ Соглашение о конфиденциальности добавлено в базу данных.")
else:
    print("⏭️ Соглашение о конфиденциальности уже существует в базе.")

conn.commit()
conn.close()