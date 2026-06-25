from fastapi import APIRouter
from app.database import get_db_connection
from app.schemas import RequestCreate, Request

router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/", response_model=Request)
def create_request(req: RequestCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO requests (name, phone, email, message) VALUES (?, ?, ?, ?)",
        (req.name, req.phone, req.email, req.message)
    )
    conn.commit()
    new_id = cursor.lastrowid
    # Получаем созданную запись
    cursor.execute("SELECT * FROM requests WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)