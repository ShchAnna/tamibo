from db_init import db
from sqlalchemy.dialects.postgresql import (
    INTEGER,
    TEXT,
    MONEY
)

class Jobs(db.Model):
    __tablename__ = "jobs"

    jobs_id = db.Column(db.INTEGER, primary_key=True)
    shipment_id = db.Column(db.INTEGER, db.ForeignKey('shipment.shipment_id'))
    jobs_tipe = db.Column(TEXT, nullable=False)
    employee = db.Column(TEXT, nullable=False)
    jobs_cost = db.Column(MONEY, nullable=False)

    def __init__(self, shipment_id, jobs_tipe, employee, jobs_cost):
        self.shipment_id = shipment_id
        self.jobs_tipe = jobs_tipe
        self.employee = employee
        self.jobs_cost = jobs_cost



    def __repr__(self):
        return f"{self.jobs_id}:{self.shipment_id}:{self.jobs_tipe}:{self.employee}:{self.jobs_cost}"