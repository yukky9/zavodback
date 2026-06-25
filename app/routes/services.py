from fastapi import APIRouter
from app.database import get_db_connection
from app.schemas import Service, ServiceCreate

router = APIRouter(prefix="/services", tags=["services"])

@router.get("/", response_model=list[Service])
def get_services():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/", response_model=Service)
def create_service(service: ServiceCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO services (title, description, icon, price) VALUES (?, ?, ?, ?)",
        (service.title, service.description, service.icon, service.price)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {**service.dict(), "id": new_id}