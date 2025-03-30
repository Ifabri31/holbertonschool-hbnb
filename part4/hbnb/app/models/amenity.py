from app.models.basemodel import BaseModel
from app import db
from sqlalchemy import Column, String, Table, Integer, ForeignKey
from sqlalchemy.orm import validates, relationship

place_amenity = db.Table(
    'place_amenity',
    Column('place_id', String, ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String, ForeignKey('amenities.id'), primary_key=True)
)

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    place = relationship('Place', secondary=place_amenity, back_populates='amenities')

    def __init__(self, name: str):
        super().__init__()
        
        self.name = name
        
    @validates('name')
    def validate_name(self, key, value: str):
        if len(value) > 50 or len(value) < 1:
            raise ValueError("Name must be 50 characters or less")
        return value