from fastapi import APIRouter, Query, HTTPException
from app.database import get_db_connection
from app.schemas import Price, PriceCreate

router = APIRouter(prefix="/prices", tags=["prices"])

@router.get("/", response_model=list[Price])
def get_prices(
    group: str = Query(None, description="Фильтр по группе"),
    search: str = Query(None, description="Поиск по названию изделия")
):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM prices WHERE 1=1"
    params = []
    if group:
        query += " AND group_name = ?"
        params.append(group)
    if search:
        query += " AND product_name LIKE ?"
        params.append(f"%{search}%")
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/", response_model=Price, status_code=201)
def create_price(price: PriceCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO prices (product_name, unit, price, price_bulk, price_retail, group_name, note)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (price.product_name, price.unit, price.price, price.price_bulk, price.price_retail, price.group_name, price.note)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM prices WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Created price not found")
    return dict(row)