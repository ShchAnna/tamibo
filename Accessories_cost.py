from db_init import db
from sqlalchemy.dialects.postgresql import (
    INTEGER,
    NUMERIC
)

class Accessories_cost(db.Model):
    __tablename__ = "accessories_cost"

    accessories_cost_id = db.Column(db.INTEGER, primary_key=True)
    shipment_id = db.Column(db.INTEGER, db.ForeignKey('shipment.shipment_id'))
    accessories_id = db.Column(db.INTEGER, db.ForeignKey('accessories.accessories_id'))
    accessories_number = db.Column(INTEGER, nullable=False)
    accessories_cost = db.Column(NUMERIC, nullable=False)

    def __init__(self, shipment_id, accessories_id, accessories_number, accessories_cost):
        self.shipment_id = shipment_id
        self.accessories_id = accessories_id
        self.accessories_number = accessories_number
        self.accessories_cost = accessories_cost


    def __repr__(self):
        return f"{self.accessories_cost_id}:{self.shipment_id}:{self.accessories_id}:{self.accessories_number}:{self.accessories_cost}"