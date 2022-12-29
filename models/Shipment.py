from db_init import db
from sqlalchemy.dialects.postgresql import (
    INTEGER,
    DATE
)


class Shipment(db.Model):
    __tablename__ = "shipment"

    shipment_id = db.Column(db.INTEGER, primary_key=True)
    model_id = db.Column(db.INTEGER, db.ForeignKey('model.model_id'))
    shipment_date = db.Column(DATE)
    products_number = db.Column(INTEGER)
    rulers_number = db.Column(INTEGER)
    delivery = db.relationship('Delivery', cascade="all, delete")
    packing = db.relationship('Packing', cascade="all, delete")
    jobs = db.relationship('Jobs', cascade="all, delete")
    accessories_cost = db.relationship('Accessories_cost', cascade="all, delete")
    materials_cost = db.relationship('Materials_cost', cascade="all, delete")

    def __init__(self, model_id, shipment_date=None, products_number=None, rulers_number=None):
        self.model_id = model_id
        self.shipment_date = shipment_date
        self.products_number = products_number
        self.rulers_number = rulers_number

    def __repr__(self):
        return f"{self.shipment_id}:{self.model_id}:{self.shipment_date}:{self.products_number}:{self.rulers_number}"

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
