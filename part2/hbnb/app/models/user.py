from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin=False):
        super().__init__()
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []
        self.reviews = []
    
    @property
    def first_name(self) -> str:
        return self._first_name
    @first_name.setter
    def first_name(self, value: str):
        if len(value) > 50 or len(value) < 1:
            raise ValueError("First name must be within 1 to 50 characters")
        self._first_name = value
        
    @property
    def last_name(self) -> str:
        return self._last_name
    @last_name.setter
    def last_name(self, value: str):
        if len(value) > 50 or len(value) < 1:
            raise ValueError("Last name must be within 1 to 50 characters")
        self._last_name = value
        
    #todo: add email validator ( buscar modulo re)
    #def email_validator()

    def add_place(self, place):
        self.places.append(place)
    
    def add_reviews(self, review):
        self.reviews.append(review)