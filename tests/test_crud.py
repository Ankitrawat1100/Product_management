import pytest
from app import create_app
from app.models import db, Product
from app.batch_calc import total_stock_threaded, total_stock_asyncio, total_stock_processes


@pytest.fixture()
def app():
    class TestConfig:
        SQLALCHEMY_DATABASE_URI = "sqlite://"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        TESTING = True
        LOG_LEVEL = "CRITICAL"
        JSON_LOGS = True
        MAIL_HOST = "localhost"
        MAIL_PORT = 2525
        MAIL_USERNAME = "x"
        MAIL_PASSWORD = "y"
        MAIL_FROM = "noreply@example.com"
        MAIL_TO = "owner@example.com"

    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        # 23 products -> batches of 10 => 3 batches (10,10,3)
        for i in range(23):
            db.session.add(Product(name=f"P{i}", qty=i + 1, price=1.0))
        db.session.commit()
    yield app


def test_totals(app):
    with app.app_context():
        t1 = total_stock_threaded(batch_size=10)
        t2 = total_stock_asyncio(batch_size=10)
        t3 = total_stock_processes(batch_size=10)
        # arithmetic series sum 1..23 = 23*24/2 = 276
        assert t1 == 276
        assert t2 == 276
        assert t3 == 276
