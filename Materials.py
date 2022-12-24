from db_init import db
from sqlalchemy.dialects.postgresql import (
    INTEGER,
    TEXT
)

class Materials(db.Model):
    __tablename__ = "materials"

    materials_id = db.Column(db.INTEGER, primary_key=True)
    model_id = db.Column(db.INTEGER, db.ForeignKey('model.model_id'))
    materials_name = db.Column(TEXT, nullable=False)
    m_per_ruler = db.Column(INTEGER, nullable=False)

    def __init__(self, model_id, materials_name, m_per_ruler):
        self.model_id = model_id
        self.materials_name = materials_name
        self.m_per_ruler = m_per_ruler


    def __repr__(self):
        return f"{self.shipment_id}:{self.model_id}:{self.shipment_date}:{self.products_number}:{self.rulers_number}"