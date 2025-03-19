from app.models.basemodel import BaseModel
from app.models.user import User
from app import db
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, ForeignKey

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), default=False)
    price = db.Column(db.Float, nullable=False, unique=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, title: str, price: float, latitude: float, longitude: float,  owner_id: str, description=None):
        super().__init__()

        self.title = title
        self.description = description
        self.price = price        
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    # @property
    # def title(self) -> str:
    #     return self._title
    # @title.setter
    @validates('title')
    def validate_title(self, key, value: str):
        if len(value) > 100 or len(value) < 1:
            raise ValueError("Title must be 100 characters or less")
        return value
    
    # @property
    # def price(self) -> float:
    #     return self._price
    # @price.setter
    @validates('price')
    def validate_price(self, key, value: float):
        if value < 0:
            raise ValueError("Price must be a positive value")
        return value

    # @property
    # def latitude(self) -> float:
    #     return self._latitude
    # @latitude.setter
    @validates('latitude')
    def validate_latitude(self, key, value: float):
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be within the range of -90 to 90")
        return value

    # @property
    # def longitude(self) -> float:
    #     return self._longitude
    # @longitude.setter
    @validates('longitude')
    def validate_longitude(self, key, value: float):
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be within the range of -180 to 180")
        return value
        
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
