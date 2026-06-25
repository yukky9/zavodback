# app/routes/__init__.py
from . import (
    products,
    services,
    rentals,
    vacancies,
    documents,
    prices,
    requests
)

# Можно также явно перечислить роутеры, чтобы их можно было импортировать как from app.routes import products, services, ...
__all__ = [
    'products',
    'services',
    'rentals',
    'vacancies',
    'documents',
    'prices',
    'requests'
]