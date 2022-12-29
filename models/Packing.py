from db_init import db
from sqlalchemy.dialects.postgresql import (
    INTEGER,
    TEXT,
    NUMERIC
)

class Packing(db.Model):
    __tablename__ = "packing"

    packing_id = db.Column(db.INTEGER, primary_key=True)
    shipment_id = db.Column(db.INTEGER, db.ForeignKey('shipment.shipment_id'))
    tags_cost = db.Column(NUMERIC, nullable=False)
    label_cost = db.Column(NUMERIC, nullable=False)
    packege_cost = db.Column(NUMERIC, nullable=False)

    def __init__(self, shipment_id, tags_cost, label_cost, packege_cost):
        self.shipment_id = shipment_id
        self.tags_cost = tags_cost
        self.label_cost = label_cost
        self.packege_cost = packege_cost



    def __repr__(self):
        return f"{self.packing_id}:{self.shipment_id}:{self.tags_cost}:{self.label_cost}:{self.packege_cost}"