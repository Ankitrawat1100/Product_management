from typing import List, Optional, Tuple
from sqlalchemy.exc import IntegrityError
from .models import db, Product
from .exceptions import ConflictError, NotFoundError, BadRequestError


def create_product(name: str, qty: int, price: float) -> Product:
    if qty < 0 or price < 0:
        raise BadRequestError("qty and price must be non-negative")
    product = Product(name=name, qty=qty, price=price)
    db.session.add(product)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ConflictError(f"Product with name '{name}' already exists") from exc
    return product


def get_product(product_id: int) -> Product:
    product = Product.query.get(product_id)
    if not product:
        raise NotFoundError(f"Product id {product_id} not found")
    return product


def list_products(offset: int = 0, limit: int = 50) -> Tuple[List[Product], int]:
    q = Product.query.order_by(Product.id.asc())
    total = q.count()
    items = q.offset(offset).limit(limit).all()
    return items, total


def update_product(product_id: int, **fields) -> Product:
    product = get_product(product_id)
    for key in ("name", "qty", "price"):
        if key in fields and fields[key] is not None:
            if key in ("qty", "price") and fields[key] < 0:
                raise BadRequestError(f"{key} must be non-negative")
            setattr(product, key, fields[key])
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise ConflictError("Duplicate product name") from exc
    return product


def delete_product(product_id: int) -> None:
    product = get_product(product_id)
    db.session.delete(product)
    db.session.commit()
