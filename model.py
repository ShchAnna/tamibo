from db_init import db
from enum import Enum, auto
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    BYTEA,
    TEXT,
    ENUM,
)


class Sizes(Enum):
    XS = auto()
    S = auto()
    M = auto()
    L = auto()
    XL = auto()


class ModelModel(db.Model):
    __tablename__ = "model"

    model_id = db.Column(db.INTEGER, primary_key=True)
    model_name = db.Column(TEXT, unique=True, nullable=False)
    article_number = db.Column(TEXT, unique=True, nullable=False)
    photo = db.Column(BYTEA)
    layout_patterns = db.Column(BYTEA)
    tailoring_technology = db.Column(TEXT)
    size_range = db.Column(ARRAY(ENUM(Sizes, name='size_ranges')))
    shipment = db.relationship('shipment',  cascade="all, delete")
    accessories = db.relationship('Accessories',  cascade="all, delete")
    materials = db.relationship('Materials',  cascade="all, delete")
    def __init__(self, model_name, article_number, photo=None, layout_patterns=None, tailoring_technology=None, size_range=None):
        self.model_name = model_name
        self.article_number = article_number
        self.photo = photo
        self.layout_patterns = layout_patterns
        self.tailoring_technology = tailoring_technology
        self.size_range = size_range

    def __repr__(self):
        return f"{self.model_id}:{self.model_name}:{self.article_number}"
