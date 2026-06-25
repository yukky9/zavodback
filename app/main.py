from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.database import init_db
from fastapi.staticfiles import StaticFiles
from app.routes import products, services, rentals, vacancies, documents, prices, requests
import os

app = FastAPI(title="Tumblers API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(products.router)
app.include_router(services.router)
app.include_router(rentals.router)
app.include_router(vacancies.router)
app.include_router(documents.router)
app.include_router(prices.router)
app.include_router(requests.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "Tumblers API is running"}

@app.get("/download-price")
async def download_price():
    file_path = os.path.join(os.path.dirname(__file__), "..", "price-otk-01-06-2026.pdf")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf", filename="price-otk-01-06-2026.pdf")
    return {"error": "Файл не найден"}