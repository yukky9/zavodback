import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.schemas import RequestCreate, Request
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/requests", tags=["requests"])

# Читаем переменные с проверкой
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM")
SMTP_TO = os.getenv("SMTP_TO")

# Вывод настроек в консоль при старте (чтобы убедиться, что всё читается)
print("📧 SMTP настройки:")
print(f"  HOST: {SMTP_HOST}")
print(f"  PORT: {SMTP_PORT}")
print(f"  USER: {SMTP_USER}")
print(f"  FROM: {SMTP_FROM}")
print(f"  TO: {SMTP_TO}")
print("=" * 40)


def send_email(subject: str, body: str, to_emails: list) -> bool:
    """Отправляет письмо через SMTP с SSL."""
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD, SMTP_FROM, SMTP_TO]):
        print("❌ Одна из переменных SMTP отсутствует. Проверьте .env")
        return False

    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        # Используем SSL-соединение
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.set_debuglevel(1)   # выводим все SMTP-команды в консоль
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM, to_emails, msg.as_string())
        print(f"✅ Письмо успешно отправлено на {', '.join(to_emails)}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ Ошибка аутентификации: неверный логин или пароль (для Gmail/Яндекса нужен пароль приложения)")
        return False
    except Exception as e:
        print(f"❌ Ошибка отправки письма: {e}")
        return False


@router.post("/", response_model=Request, status_code=201)
def create_request(req: RequestCreate):
    # 1. Сохраняем в БД
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO requests (name, phone, email, message) VALUES (?, ?, ?, ?)",
        (req.name, req.phone, req.email, req.message)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM requests WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    # 2. Проверяем, есть ли кому отправлять
    if not SMTP_TO:
        print("⚠️ SMTP_TO не задан, письмо не отправлено.")
        return dict(row)

    recipients = [email.strip() for email in SMTP_TO.split(",") if email.strip()]
    if not recipients:
        print("⚠️ SMTP_TO не содержит корректных адресов")
        return dict(row)

    # 3. Формируем письмо
    subject = f"Новая заявка от {req.name}"
    body = f"""
Поступила новая заявка с сайта:

Имя: {req.name}
Телефон: {req.phone}
Email отправителя: {req.email or 'не указан'}
Сообщение: {req.message or 'не указано'}

---
Дата: {row['created_at']}
    """

    # 4. Отправляем письмо
    send_email(subject, body, recipients)

    return dict(row)


@router.get("/", response_model=list[Request])
def get_requests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]