from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        
        if len(name) > 50:
            raise ValueError("Name must be 50 characters or less")
        self.name = name
        self.amenities = []
    
    def add_amenity(self, amenity):
        """Add amenity to the amenity list"""
        self.amenities.append(amenity)