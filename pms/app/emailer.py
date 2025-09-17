import logging
import smtplib
from email.message import EmailMessage
from threading import Thread
from flask import current_app
from .models import Product

log = logging.getLogger(__name__)


def _send_email(product: Product):
    cfg = current_app.config
    msg = EmailMessage()
    msg["Subject"] = f"New Product Created: {product.name}"
    msg["From"] = cfg["MAIL_FROM"]
    msg["To"] = cfg["MAIL_TO"]
    msg.set_content(
        f"A new product was created:\n\n"
        f"ID: {product.id}\nName: {product.name}\nQty: {product.qty}\nPrice: {product.price}\n"
    )
    try:
        with smtplib.SMTP(cfg["MAIL_HOST"], cfg["MAIL_PORT"]) as smtp:
            smtp.login(cfg["MAIL_USERNAME"], cfg["MAIL_PASSWORD"])
            smtp.send_message(msg)
            log.info("email.sent", extra={"product_id": product.id})
    except Exception as exc:  # noqa: BLE001
        log.exception("email.failed", extra={"error": str(exc)})


def send_new_product_email_bg(product: Product):
    # Background thread; app context preserved by using current_app._get_current_object() only for config read.
    t = Thread(target=_send_email, args=(product,), daemon=True)
    t.start()
