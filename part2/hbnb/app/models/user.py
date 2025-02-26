from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin=False):
        super().__init__()
        
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("First name and last name must be maximum 50 characters")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []
        self.reviews = []
    
    def add_place(self, place):
        self.places.append(place)
    
    def add_reviews(self, review):
        self.reviews.append(review)