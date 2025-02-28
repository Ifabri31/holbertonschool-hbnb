from app.models.basemodel import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title: str, price: float, latitude: float, longitude: float,  owner_id: str, description=""):
        super().__init__()

        self.title = title
        self.description = description
        self.price = price        
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    @property
    def title(self) -> str:
        return self._title
    @title.setter
    def title(self, value: str):
        if len(value) > 100 or len(value) < 1:
            raise ValueError("Title must be 100 characters or less")
        self._title = value
    
    @property
    def price(self) -> float:
        return self._price
    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price must be a positive value")
        self._price = value

    @property
    def latitude(self) -> float:
        return self._latitude
    @latitude.setter
    def latitude(self, value: float):
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be within the range of -90 to 90")
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude
    @longitude.setter
    def longitude(self, value: float):
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be within the range of -180 to 180")
        self._longitude = value
        
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
