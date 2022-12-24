from db_init import db
from sqlalchemy.dialects.postgresql import (
    INTEGER,
    TEXT,
    MONEY
)

class Packing(db.Model):
    __tablename__ = "packing"

    packing_id = db.Column(db.INTEGER, primary_key=True)
    shipment_id = db.Column(db.INTEGER, db.ForeignKey('shipment.shipment_id'))
    tags_cost = db.Column(MONEY, nullable=False)
    label_cost = db.Column(MONEY, nullable=False)
    packege_cost = db.Column(MONEY, nullable=False)

    def __init__(self, shipment_id, tags_cost, label_cost, packege_cost):
        self.shipment_id = shipment_id
        self.tags_cost = tags_cost
        self.label_cost = label_cost
        self.packege_cost = packege_cost



    def __repr__(self):
        return f"{self.shipment_id}:{self.model_id}:{self.shipment_date}:{self.products_number}:{self.rulers_number}"