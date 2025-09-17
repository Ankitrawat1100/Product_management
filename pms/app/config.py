"""
config.py
----------
Centralized configuration file for Flask app.
Defines database URI, SMTP settings, and logging configuration.
"""

import os

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SMTP / Mailtrap (or any SMTP)
    MAIL_HOST = os.getenv("MAIL_HOST", "sandbox.smtp.mailtrap.io")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "2525"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "YOUR_USER")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "YOUR_PASS")
    MAIL_FROM = os.getenv("MAIL_FROM", "noreply@example.com")
    MAIL_TO = os.getenv("MAIL_TO", "owner@example.com")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    JSON_LOGS = os.getenv("JSON_LOGS", "1") == "1"