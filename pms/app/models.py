from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    qty = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(Numeric(10, 2), nullable=False, default=0)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "qty": self.qty, "price": float(self.price)}
