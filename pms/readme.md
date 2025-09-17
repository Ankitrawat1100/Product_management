# Product Management Service (pms)

A production-ready, multi-module Python API and client:

- **Flask REST API** with CRUD for `Product {id, name, qty, price}`
- **SQLite** persistence (file: `db.sqlite` by default)
- **Immediate email** notification (background thread) on product creation
- **Batch stock calculations** in batches of 10 via threads, processes, **and** asyncio
- **Scraper** (requests + BeautifulSoup) to seed the DB from product pages
- **Structured JSON logging** and centralized exception handling
- **PEP 8** and `pylint` friendly
- **Unit tests** with `pytest`
- Minimal **CLI client** to hit the API

## Quick Start

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

# Configure SMTP (Mailtrap or similar)
export MAIL_HOST=sandbox.smtp.mailtrap.io
export MAIL_PORT=2525
export MAIL_USERNAME=XXXX
export MAIL_PASSWORD=YYYY
export MAIL_FROM=noreply@example.com
export MAIL_TO=owner@example.com

export JSON_LOGS=1
export LOG_LEVEL=INFO
