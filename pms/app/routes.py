"""
routes.py
----------
Defines Flask API routes for CRUD operations and batch stock calculation.
"""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import HTTPException
from .crud import (
    create_product, get_product, list_products, update_product, delete_product
)
from .emailer import send_new_product_email_bg
from .batch_calc import (
    total_stock_threaded, total_stock_processes, total_stock_asyncio
)
from .scraper import scrape_and_seed

bp = Blueprint("api", __name__)


@bp.post("/products")
def create_product_route():
    """
    Create a new product and trigger email notification.
    """
    data = request.get_json(force=True, silent=True) or {}
    product = create_product(
        name=data.get("name"),
        qty=int(data.get("qty", 0)),
        price=float(data.get("price", 0.0)),
    )
    # Fire-and-forget background email
    send_new_product_email_bg(product)
    return jsonify(product=product.to_dict()), 201


@bp.get("/products/<int:pid>")
def get_product_route(pid: int):
    product = get_product(pid)
    return jsonify(product=product.to_dict())


@bp.get("/products")
def list_products_route():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 50))
    items, total = list_products(offset, limit)
    return jsonify(
        items=[p.to_dict() for p in items],
        total=total,
        offset=offset,
        limit=limit
    )


@bp.patch("/products/<int:pid>")
def update_product_route(pid: int):
    data = request.get_json(force=True, silent=True) or {}
    product = update_product(
        pid,
        name=data.get("name"),
        qty=data.get("qty"),
        price=data.get("price"),
    )
    return jsonify(product=product.to_dict())


@bp.delete("/products/<int:pid>")
def delete_product_route(pid: int):
    delete_product(pid)
    return jsonify(message="deleted"), 204


@bp.post("/stock/total")
def total_stock_route():
    """
    body: {"mode": "threads" | "processes" | "asyncio"}
    Calculates sum of qty in batches of 10.
    """
    mode = (request.get_json(silent=True) or {}).get("mode", "threads")
    if mode == "threads":
        result = total_stock_threaded(batch_size=10)
    elif mode == "processes":
        result = total_stock_processes(batch_size=10)
    elif mode == "asyncio":
        result = total_stock_asyncio(batch_size=10)
    else:
        raise HTTPException(description="invalid mode", response=None)
    return jsonify(total_stock=result)


@bp.post("/scrape/seed")
def scrape_seed_route():
    """
    body: {"url": "https://example.com/products"}
    Scrapes product cards and seeds DB.
    """
    data = request.get_json(silent=True) or {}
    url = data.get("url")
    added = scrape_and_seed(url)
    return jsonify(added=[p.to_dict() for p in added]), 201
