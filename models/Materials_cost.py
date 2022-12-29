from db_init import db
from sqlalchemy.dialects.postgresql import (
    NUMERIC,
)

class Materials_cost(db.Model):
    __tablename__ = "materials_cost"

    materials_cost_id = db.Column(db.INTEGER, primary_key=True)
    shipment_id = db.Column(db.INTEGER, db.ForeignKey('shipment.shipment_id'))
    materials_id = db.Column(db.INTEGER, db.ForeignKey('materials.materials_id'))
    materials_number = db.Column(NUMERIC, nullable=False)
    materials_cost = db.Column(NUMERIC, nullable=False)

    def __init__(self, shipment_id, materials_id, materials_number, materials_cost):
        self.shipment_id = shipment_id
        self.materials_id = materials_id
        self.materials_number = materials_number
        self.materials_cost = materials_cost


    def __repr__(self):
        return f"{self.materials_cost_id}:{self.shipment_id}:{self.materials_id}:{self.materials_number}:{self.materials_cost}"