"""
batch_calc.py
--------------
Implements total stock calculation using threading, processes, and asyncio.
"""

import asyncio
import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List
from .models import Product


def _sum_qty(products: List[Product]) -> int:
    return sum(p.qty for p in products)


def _fetch_all_products() -> List[Product]:
    # Lazy import to avoid circular app refs
    return Product.query.order_by(Product.id.asc()).all()


def _batches(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def total_stock_threaded(batch_size: int = 10) -> int:
    """
    Calculate total stock using ThreadPoolExecutor.
    """
    
    products = _fetch_all_products()
    total = 0
    with ThreadPoolExecutor() as pool:
        totals = list(pool.map(_sum_qty, _batches(products, batch_size)))
    total = sum(totals)
    return total


def total_stock_processes(batch_size: int = 10) -> int:
    products = _fetch_all_products()
    with ProcessPoolExecutor() as pool:
        totals = list(pool.map(lambda b: sum(p.qty for p in b), _batches(products, batch_size)))
    return sum(totals)


async def _async_sum(products: List[Product]) -> int:
    # Simulate async workload; real life might await I/O (e.g., remote calls)
    await asyncio.sleep(0)
    return sum(p.qty for p in products)


def total_stock_asyncio(batch_size: int = 10) -> int:
    products = _fetch_all_products()
    batches = list(_batches(products, batch_size))

    async def runner():
        coros = [_async_sum(b) for b in batches]
        results = await asyncio.gather(*coros)
        return sum(results)
    
    return asyncio.run(runner())