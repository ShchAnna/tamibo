from db_init import db
from sqlalchemy.dialects.postgresql import (
    INTEGER,
    TEXT
)

class Accessories(db.Model):
    __tablename__ = "accessories"

    accessories_id = db.Column(db.INTEGER, primary_key=True)
    model_id = db.Column(db.INTEGER, db.ForeignKey('model.model_id'))
    accessories_name = db.Column(TEXT, nullable=False)
    number_per_one = db.Column(INTEGER, nullable=False)

    def __init__(self, model_id, accessories_name, number_per_one):
        self.model_id = model_id
        self.accessories_name = accessories_name
        self.number_per_one = number_per_one


    def __repr__(self):
        return f"{self.accessories_id}:{self.model_id}:{self.accessories_name}:{self.number_per_one}"