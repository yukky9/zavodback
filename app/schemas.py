from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Products ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

# --- Services ---
class ServiceBase(BaseModel):
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None
    price: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int
    class Config:
        orm_mode = True

# --- Rentals ---
class RentalBase(BaseModel):
    title: str
    description: Optional[str] = None
    area: Optional[str] = None
    price: Optional[str] = None
    image_url: Optional[str] = None

class RentalCreate(RentalBase):
    pass

class Rental(RentalBase):
    id: int
    class Config:
        orm_mode = True

# --- Vacancies ---
class VacancyBase(BaseModel):
    title: str
    description: Optional[str] = None
    salary: Optional[str] = None
    requirements: Optional[str] = None

class VacancyCreate(VacancyBase):
    pass

class Vacancy(VacancyBase):
    id: int
    class Config:
        orm_mode = True

# --- Documents ---
class DocumentBase(BaseModel):
    title: str
    doc_type: str
    file_url: Optional[str] = None
    date: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    class Config:
        orm_mode = True

# --- Prices (обновлённый) ---
class PriceBase(BaseModel):
    product_name: str
    unit: Optional[str] = None
    price: Optional[float] = None
    price_bulk: Optional[float] = None
    price_retail: Optional[float] = None
    group_name: Optional[str] = None
    note: Optional[str] = None

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    id: int
    class Config:
        orm_mode = True

# --- Requests ---
class RequestBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    message: Optional[str] = None

class RequestCreate(RequestBase):
    pass

class Request(RequestBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True