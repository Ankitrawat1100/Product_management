import pytest
from flask import Flask
from app import create_app
from app.models import db, Product


@pytest.fixture()
def app():
    class TestConfig:
        SQLALCHEMY_DATABASE_URI = "sqlite://"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        TESTING = True
        MAIL_HOST = "localhost"
        MAIL_PORT = 2525
        MAIL_USERNAME = "x"
        MAIL_PASSWORD = "y"
        MAIL_FROM = "noreply@example.com"
        MAIL_TO = "owner@example.com"
        LOG_LEVEL = "CRITICAL"
        JSON_LOGS = True

    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_create_and_get_product(client):
    resp = client.post("/api/products", json={"name": "A", "qty": 5, "price": 9.99})
    assert resp.status_code == 201
    pid = resp.get_json()["product"]["id"]

    resp2 = client.get(f"/api/products/{pid}")
    assert resp2.status_code == 200
    data = resp2.get_json()["product"]
    assert data["name"] == "A"
    assert data["qty"] == 5
    assert data["price"] == 9.99


def test_update_and_delete(client):
    r = client.post("/api/products", json={"name": "B", "qty": 1, "price": 1.0})
    pid = r.get_json()["product"]["id"]
    ru = client.patch(f"/api/products/{pid}", json={"qty": 7})
    assert ru.status_code == 200
    assert ru.get_json()["product"]["qty"] == 7

    rd = client.delete(f"/api/products/{pid}")
    assert rd.status_code in (200, 204)

    r404 = client.get(f"/api/products/{pid}")
    assert r404.status_code == 404
