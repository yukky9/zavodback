# add_financial_reports.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")

docs = [
    {
        "title": "Финансовый отчёт за 2020 год",
        "file": "/static/docs/buh_report_2020.pdf",
        "date": "2020-12-31"
    },
    {
        "title": "Финансовый отчёт за 2021 год",
        "file": "/static/docs/buh_report_2021.pdf",
        "date": "2021-12-31"
    },
    {
        "title": "Финансовый отчёт за 2022 год",
        "file": "/static/docs/buh_report_2022.pdf",
        "date": "2022-12-31"
    },
    {
        "title": "Финансовый отчёт за 2023 год (в разработке)",
        "file": "#",  # заглушка – ссылка ведёт на текущую страницу
        "date": "2023-12-31"
    },
    {
        "title": "Финансовый отчёт за 2024 год (в разработке)",
        "file": "#",
        "date": "2024-12-31"
    }
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Проверяем, есть ли уже такие документы (чтобы не дублировать)
for doc in docs:
    cursor.execute(
        "SELECT id FROM documents WHERE title = ? AND doc_type = 'Финансовый отчет'",
        (doc["title"],)
    )
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO documents (title, doc_type, file_url, date) VALUES (?, ?, ?, ?)",
            (doc["title"], "Финансовый отчет", doc["file"], doc["date"])
        )
        print(f"✅ Добавлен: {doc['title']}")
    else:
        print(f"⏭️ Уже существует: {doc['title']}")

conn.commit()
conn.close()
print("🎉 Финансовые отчёты загружены в базу данных.")