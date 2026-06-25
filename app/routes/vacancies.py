from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.schemas import Vacancy, VacancyCreate

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

@router.get("/", response_model=list[Vacancy])
def get_vacancies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vacancies")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/", response_model=Vacancy, status_code=201)
def create_vacancy(vacancy: VacancyCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vacancies (title, description, salary, requirements) VALUES (?, ?, ?, ?)",
        (vacancy.title, vacancy.description, vacancy.salary, vacancy.requirements)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM vacancies WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Created vacancy not found")
    return dict(row)