from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.schemas import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[Product])
def get_products(category: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if category:
        cursor.execute("SELECT * FROM products WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/", response_model=Product)
def create_product(product: ProductCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, description, image_url, category, price) VALUES (?, ?, ?, ?, ?)",
        (product.name, product.description, product.image_url, product.category, product.price)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {**product.dict(), "id": new_id}