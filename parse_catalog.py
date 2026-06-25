# backend/parse_catalog.py
import pdfplumber
import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")

def extract_products_from_pdf(pdf_path):
    """
    Извлекает из PDF названия изделий и их группы (цены не извлекаются).
    Возвращает список словарей: {'name': ..., 'category': ..., 'description': ...}
    """
    products = []
    current_category = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Определяем категорию по ключевым словам (заголовки разделов)
                if 'ТУМБЛЕРЫ' in line or 'КНОПКИ' in line or 'ПЕРЕКЛЮЧАТЕЛИ' in line or 'ВЫКЛЮЧАТЕЛИ' in line:
                    current_category = line
                    continue

                # Ищем названия изделий (шаблон: буквы + цифры + дефисы/точки)
                match = re.search(r'\b([A-ZА-Я]{1,3}[0-9\-\.]+[A-ZА-Я0-9\-\.]*)\b', line)
                if match:
                    product_name = match.group(0)
                    if len(product_name) > 1 and not product_name.isdigit():
                        description = line.replace(product_name, '').strip()
                        if not description:
                            description = f"Изделие из группы {current_category or 'Общая'}"
                        products.append({
                            'name': product_name,
                            'category': current_category or 'Общая',
                            'description': description[:200]
                        })

    # Удаляем дубликаты (по имени)
    unique = {}
    for p in products:
        if p['name'] not in unique:
            unique[p['name']] = p
    return list(unique.values())

def save_products_to_db(products):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Очищаем таблицу, чтобы избежать дублей (или можно добавить проверку)
    cursor.execute("DELETE FROM products")

    for p in products:
        # price = NULL (оставляем без цены)
        cursor.execute(
            "INSERT INTO products (name, description, image_url, category, price) VALUES (?, ?, ?, ?, ?)",
            (p['name'], p['description'], 'https://via.placeholder.com/150?text=' + p['name'][:10], p['category'], None)
        )

    conn.commit()
    conn.close()
    print(f"✅ Загружено {len(products)} товаров без цен.")

if __name__ == "__main__":
    pdf_file = "catalog.pdf"  # или "catalog.pdf"
    if not os.path.exists(pdf_file):
        print(f"❌ Файл {pdf_file} не найден. Поместите его в папку backend/")
    else:
        print("🔍 Начинаем парсинг каталога...")
        products = extract_products_from_pdf(pdf_file)
        print(f"🔍 Извлечено {len(products)} уникальных наименований.")
        if products:
            save_products_to_db(products)
        else:
            print("⚠️ Не удалось извлечь товары. Возможно, структура PDF не распознаётся.")