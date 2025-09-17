"""
scraper.py
-----------
Scrapes product data from e-commerce pages using requests + BeautifulSoup.
"""

import logging
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from flask import current_app
from .crud import create_product

log = logging.getLogger(__name__)


def parse_products(html: str):
    """
    Expects cards like:
      <div class="product">
        <h3 class="name">Widget A</h3>
        <span class="qty">12</span>
        <span class="price">9.99</span>
      </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for card in soup.select(".product"):
        name = (card.select_one(".name") or {}).get_text(strip=True)
        qty = (card.select_one(".qty") or {}).get_text(strip=True)
        price = (card.select_one(".price") or {}).get_text(strip=True)
        if not name:
            continue
        try:
            items.append({"name": name, "qty": int(qty), "price": float(price)})
        except ValueError:
            # Skip malformed entries, but keep scraping
            continue
    return items


def scrape_and_seed(url: Optional[str]) -> List[dict]:
    if not url:
        raise ValueError("url is required")
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    parsed = parse_products(resp.text)
    added = []
    for it in parsed:
        try:
            p = create_product(**it)
            added.append(p)
        except Exception as exc:  # noqa: BLE001
            log.warning("scrape.seed.skip", extra={"name": it.get("name"), "error": str(exc)})
    return added
