from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.schemas import Document, DocumentCreate

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/", response_model=list[Document])
def get_documents(doc_type: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if doc_type:
        cursor.execute("SELECT * FROM documents WHERE doc_type = ?", (doc_type,))
    else:
        cursor.execute("SELECT * FROM documents")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/", response_model=Document, status_code=201)
def create_document(document: DocumentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documents (title, doc_type, file_url, date) VALUES (?, ?, ?, ?)",
        (document.title, document.doc_type, document.file_url, document.date)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute("SELECT * FROM documents WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Created document not found")
    return dict(row)