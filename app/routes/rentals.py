from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.schemas import Rental, RentalCreate

router = APIRouter(prefix="/rentals", tags=["rentals"])

@router.get("/", response_model=list[Rental])
def get_rentals():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rentals")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/", response_model=Rental, status_code=201)
def create_rental(rental: RentalCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO rentals (title, description, area, price, image_url) VALUES (?, ?, ?, ?, ?)",
        (rental.title, rental.description, rental.area, rental.price, rental.image_url)
    )
    conn.commit()
    new_id = cursor.lastrowid
    # Возвращаем созданную запись
    cursor.execute("SELECT * FROM rentals WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Created rental not found")
    return dict(row)