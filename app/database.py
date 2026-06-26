import sqlite3
import os

DB_PATH = os.getenv(
    "DB_PATH",
    os.path.join(os.path.dirname(__file__), "..", "db.sqlite3"),
)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def column_exists(cursor, table, column):
    """Проверяет, существует ли колонка в таблице."""
    cursor.execute(f"PRAGMA table_info({table})")
    return any(col[1] == column for col in cursor.fetchall())

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # --- Таблица products (без изменений) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            image_url TEXT,
            category TEXT,
            price REAL
        )
    ''')

    # --- Таблица services (без изменений) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            price TEXT
        )
    ''')

    # --- Таблица rentals (без изменений) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            area TEXT,
            price TEXT,
            image_url TEXT
        )
    ''')

    # --- Таблица vacancies (без изменений) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            salary TEXT,
            requirements TEXT
        )
    ''')

    # --- Таблица documents (без изменений) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            doc_type TEXT,
            file_url TEXT,
            date TEXT
        )
    ''')

    # --- Таблица prices (с новыми полями и миграцией) ---
    # Проверяем, существует ли таблица
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prices'")
    table_exists = cursor.fetchone() is not None

    if not table_exists:
        # Создаём таблицу с новыми полями
        cursor.execute('''
            CREATE TABLE prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                unit TEXT,
                price REAL,
                price_bulk REAL,
                price_retail REAL,
                group_name TEXT,
                note TEXT
            )
        ''')
    else:
        # Если таблица существует, добавляем недостающие колонки
        if not column_exists(cursor, 'prices', 'price_bulk'):
            cursor.execute("ALTER TABLE prices ADD COLUMN price_bulk REAL")
        if not column_exists(cursor, 'prices', 'price_retail'):
            cursor.execute("ALTER TABLE prices ADD COLUMN price_retail REAL")
        if not column_exists(cursor, 'prices', 'group_name'):
            cursor.execute("ALTER TABLE prices ADD COLUMN group_name TEXT")
        # также можно добавить unit и note, если их нет
        if not column_exists(cursor, 'prices', 'unit'):
            cursor.execute("ALTER TABLE prices ADD COLUMN unit TEXT")
        if not column_exists(cursor, 'prices', 'note'):
            cursor.execute("ALTER TABLE prices ADD COLUMN note TEXT")

    # --- Таблица requests (без изменений) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Заполнение тестовыми данными (только если таблицы пусты) ---
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO products (name, description, image_url, category, price) VALUES (?, ?, ?, ?, ?)",
            [
                ("Тумблер ТП1-2", "Двухпозиционный тумблер, 10А", "https://via.placeholder.com/150", "тумблеры", 120.50),
                ("Переключатель П2Т-1", "Галетный переключатель", "https://via.placeholder.com/150", "переключатели", 85.00),
                ("Кнопка КМ1-1", "Кнопка управления с фиксацией", "https://via.placeholder.com/150", "кнопки", 45.30),
                ("Реле РП-21", "Электромагнитное реле", "https://via.placeholder.com/150", "реле", 210.00),
            ]
        )

    cursor.execute("SELECT COUNT(*) FROM services")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO services (title, description, icon, price) VALUES (?, ?, ?, ?)",
            [
                ("Химическое никелирование", "Нанесение химического никелевого покрытия", "🔬", "по запросу"),
                ("Гальванопокрытие деталей", "Гальваническое покрытие металлических деталей", "⚡", "по запросу"),
                ("Химическое оксидирование", "Химическое оксидирование для создания защитных покрытий", "🧪",
                 "по запросу"),
                ("Цинкование", "Цинкование деталей для антикоррозионной защиты", "🔩", "по запросу"),
                ("Никелирование", "Никелирование для придания декоративного блеска", "✨", "по запросу"),
                ("Покрытие сплавом олово-висмут", "Нанесение покрытия из сплава олово-висмут", "🛡️", "по запросу"),
                ("Осветление из меди и латуни", "Осветление и обработка деталей из меди и латуни", "🌟", "по запросу"),
                ("Изготовление деталей из пластмассы", "Производство пластмассовых деталей по чертежам", "🧩",
                 "по запросу"),
                ("Электроэрозионные работы", "Электроэрозионная обработка для изготовления пресс-форм", "⚙️",
                 "по запросу"),
                ("Проектирование и изготовление штампов", "Полный цикл проектирования и изготовления штампов", "🔧",
                 "по запросу"),
                ("Эксплуатация а/м КАМАЗ, ГАЗель", "Предоставление автотранспортных услуг", "🚛", "по запросу"),
                ("Термообработка деталей", "Термическая обработка для повышения прочности", "🔥", "по запросу"),
            ]
        )

    cursor.execute("SELECT COUNT(*) FROM rentals")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO rentals (title, description, area, price, image_url) VALUES (?, ?, ?, ?, ?)",
            [
                ("Производственный цех №3", "Площадь 500 м², высокие потолки", "500 м²", "150 000 ₽/мес", "https://via.placeholder.com/300"),
                ("Складской комплекс", "Отапливаемый склад, 200 м²", "200 м²", "80 000 ₽/мес", "https://via.placeholder.com/300"),
            ]
        )

    cursor.execute("SELECT COUNT(*) FROM vacancies")
    if cursor.fetchone()[0] == 0:
        # Реальные вакансии с сайта
        real_vacancies = [
            {
                "title": "Инженер-руководитель группы",
                "description": "Организовывать работу персонала, контролировать качество испытаний, оформлять документацию, составлять график смен, аттестовывать оборудование.",
                "requirements": "образование высшее техническое (стаж не менее 1 года) или среднее спец (не менее 3 лет); знания по организации труда и проведению испытаний; до 60 лет (желательно); коммуникабельность, дисциплинарность.",
                "salary": "по договорённости"
            },
            {
                "title": "Инженер-технолог",
                "description": "Внедрять и совершенствовать техническую документацию на оснастку; составлять план размещения оборудования; анализировать причины брака.",
                "requirements": "образование — высшее техническое без требований к стажу ИЛИ среднее профессиональное + стаж в должности инженера-технолога не менее 3 лет.",
                "salary": "по договорённости"
            },
            {
                "title": "Кладовщик",
                "description": "Организовывать получение, выдачу, хранение, учёт, списание оснастки и инструмента; заполнять документы в 1С; проводить инвентаризацию.",
                "requirements": "образование – не ниже среднего.",
                "salary": "по договорённости"
            },
            {
                "title": "Оператор станков с программным управлением 3 разряда (ученик)",
                "description": "Обрабатывать детали средней сложности; наблюдать за работой станков; устанавливать и снимать детали; проверять размеры.",
                "requirements": "образование — высшее техническое или среднее профессиональное (техническое).",
                "salary": "по договорённости"
            },
            {
                "title": "Инженер по промышленной безопасности",
                "description": "Контролировать выполнение требований промышленной безопасности; участвовать в расследовании аварий; участвовать в мероприятиях по безопасности.",
                "requirements": "образование — высшее техническое, опыт – не менее 3 лет на опасном производственном объекте.",
                "salary": "по договорённости"
            },
            {
                "title": "Слесарь-сантехник 4 разряда",
                "description": "Ремонтировать и разрабатывать сантехнические системы предприятия.",
                "requirements": "опыт работы – от 3 лет.",
                "salary": "по договорённости"
            },
            {
                "title": "Транспортировщик",
                "description": "Перевозить грузы вручную или на электрокаре; доставлять химические материалы; укладывать и сортировать грузы.",
                "requirements": "водительские права.",
                "salary": "по договорённости"
            },
            {
                "title": "Машинист экскаватора",
                "description": "Управлять и обслуживать экскаватор-погрузчик МТЗ-92, грейдер ДЗ-143.",
                "requirements": "опыт работы – от 2 лет; права категории В, С, D, Е, F (с отметкой тракторист-машинист, машинист экскаватора).",
                "salary": "по договорённости"
            },
            {
                "title": "Монтажник РЭАиП (ученик)",
                "description": "Выполнение постановленных задач.",
                "requirements": "без особых требований.",
                "salary": "по договорённости"
            },
            {
                "title": "Фрезеровщик 3 разряда (ученик)",
                "description": "Фрезеровать сложные детали; обрабатывать крупные детали; выполнять расчёты для фрезерования зубьев шестерен.",
                "requirements": "без особых требований.",
                "salary": "по договорённости"
            },
            {
                "title": "Зав.складом готовых деталей ПДО",
                "description": "Принимать детали из заготовительных цехов, хранить на складе, выдавать в сборочный цех.",
                "requirements": "образование — не ниже среднего; навыки работы в 1С «Комплексная».",
                "salary": "по договорённости"
            },
            {
                "title": "Распределитель работ",
                "description": "Организовывать движение деталей; заполнять документы в 1С; проводить инвентаризацию.",
                "requirements": "образование — не ниже среднего.",
                "salary": "по договорённости"
            },
            {
                "title": "Контролер деталей и приборов",
                "description": "Контролировать техническое изготовление деталей на соответствие документации.",
                "requirements": "образование — не ниже среднего.",
                "salary": "по договорённости"
            },
            {
                "title": "Испытатель деталей и приборов",
                "description": "Проводить монтаж и демонтаж изделий; проводить испытания; контролировать исправность оборудования.",
                "requirements": "образование — не ниже среднего.",
                "salary": "по договорённости"
            }
        ]

        for vac in real_vacancies:
            cursor.execute(
                "INSERT INTO vacancies (title, description, salary, requirements) VALUES (?, ?, ?, ?)",
                (vac["title"], vac["description"], vac["salary"], vac["requirements"])
            )

    cursor.execute("SELECT COUNT(*) FROM documents")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO documents (title, doc_type, file_url, date) VALUES (?, ?, ?, ?)",
            [
                ("Годовой отчёт 2025", "Годовые отчеты", "/docs/annual_2025.pdf", "2025-12-31"),
                ("Финансовая отчётность Q4", "Финансовые отчеты", "/docs/financial_q4.pdf", "2025-12-31"),
                ("Раскрытие информации о сделках", "Раскрытие информации", "/docs/disclosure.pdf", "2025-11-15"),
                ("Спецоценка труда 2025", "Специальная оценка труда", "/docs/special_assessment.pdf", "2025-10-01"),
            ]
        )

    conn.commit()
    conn.close()