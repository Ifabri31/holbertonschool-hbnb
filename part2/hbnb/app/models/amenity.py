from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        
        self.name = name
        
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, value: str):
        if len(value) > 50 or len(value) < 1:
            raise ValueError("Name must be 50 characters or less")
        self._name = value