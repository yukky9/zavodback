# add_sout_docs.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")

docs = [
    {"title": "Специальная оценка условий труда 2020", "file": "/static/docs/sout_2020.pdf", "date": "2020-12-31"},
    {"title": "Специальная оценка условий труда 2021", "file": "/static/docs/sout_2021.pdf", "date": "2021-12-31"},
    {"title": "Специальная оценка условий труда 2022", "file": "/static/docs/sout_2022.pdf", "date": "2022-12-31"},
    {"title": "Специальная оценка условий труда 2023", "file": "/static/docs/sout_2023.pdf", "date": "2023-12-31"},
    {"title": "Специальная оценка условий труда 2024", "file": "/static/docs/sout_2024.pdf", "date": "2024-12-31"},
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for doc in docs:
    cursor.execute(
        "INSERT INTO documents (title, doc_type, file_url, date) VALUES (?, ?, ?, ?)",
        (doc["title"], "СОУТ", doc["file"], doc["date"])
    )

conn.commit()
conn.close()
print("✅ Документы СОУТ добавлены в базу данных.")