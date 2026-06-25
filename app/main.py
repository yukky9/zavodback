from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

from app.database import init_db
from app.routes import products, services, rentals, vacancies, documents, prices, requests

app = FastAPI(title="Tumblers API")

# Настройка CORS (разрешаем запросы с фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация базы данных при старте
@app.on_event("startup")
def startup():
    init_db()

# Подключаем все роутеры
app.include_router(products.router)
app.include_router(services.router)
app.include_router(rentals.router)
app.include_router(vacancies.router)
app.include_router(documents.router)
app.include_router(prices.router)
app.include_router(requests.router)  # ← роут для заявок

# Раздача статических файлов (PDF, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Эндпоинт для скачивания прайс-листа
@app.get("/download-price")
async def download_price():
    file_path = os.path.join(os.path.dirname(__file__), "..", "price-otk-01-06-2026.pdf")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf", filename="price-otk-01-06-2026.pdf")
    return {"error": "Файл не найден"}

# Корневой эндпоинт
@app.get("/")
def root():
    return {"message": "Tumblers API is running"}