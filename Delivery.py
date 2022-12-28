from db_init import db
from sqlalchemy.dialects.postgresql import (
    INTEGER,
    TEXT,
    NUMERIC
)

class Delivery(db.Model):
    __tablename__ = "delivery"

    delivery_id = db.Column(db.INTEGER, primary_key=True)
    shipment_id = db.Column(db.INTEGER, db.ForeignKey('shipment.shipment_id'))
    from_where = db.Column(TEXT, nullable=False)
    to_where = db.Column(TEXT, nullable=False)
    tipe_delivery = db.Column(TEXT, nullable=False)
    object_delivery = db.Column(TEXT, nullable=False)
    delivery_cost = db.Column(NUMERIC, nullable=False)


    def __init__(self, shipment_id, from_where, to_where, tipe_delivery, object_delivery, delivery_cost):
        self.shipment_id = shipment_id
        self.from_where = from_where
        self.to_where = to_where
        self.tipe_delivery = tipe_delivery
        self.object_delivery = object_delivery
        self.delivery_cost = delivery_cost

    def __repr__(self):
        return f"{self.delivery_id}:{self.shipment_id}:{self.from_where}:{self.to_where}:{self.tipe_delivery}:{self.object_delivery}:{self.delivery_cost}"