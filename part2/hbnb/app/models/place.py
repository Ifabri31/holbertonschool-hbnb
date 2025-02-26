from app.models.basemodel import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title: str, price: float, latitude: float, longitude: float,  owner: User, description=""):
        super().__init__()

        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")
        self.title = title
        self.description = description

        if price < 0:
            raise ValueError("Price must be a positive value")
        self.price = price
        
        if latitude < -90.0 and latitude > 90.0:
            raise ValueError("Latitude must be within the range of -90 to 90")
        self.latitude = latitude

        if longitude < -180.0 and longitude > 180.0:
            raise ValueError("Longitude must be within the range of -180 to 180")
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
        
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

# Lorena = User("Lorena", "Leon", "dasd", "asd")        
# girasoles = Place("Girasoles", 20.0, 23.0, -120.0, Lorena)

# print(girasoles.owner.updated_at)