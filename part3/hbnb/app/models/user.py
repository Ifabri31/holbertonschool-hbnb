from app.models.basemodel import BaseModel
import re
from app import db, bcrypt
from sqlalchemy.orm import validates, relationship

#bcrypt = Bcrypt()


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 
    reviews = relationship('Review', back_populates='user')
    place = relationship('Place', back_populates='owner')

    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin=False):
        super().__init__()
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = int(is_admin)
        self.places = []
        self.reviews = []
    
    @validates('first_name')
    def validate_first_name(self, key, value: str):
        if len(value) > 50 or len(value) < 1:
            raise ValueError("First name must be within 1 to 50 characters")
        return value
        
    @validates('last_name')
    def validate_last_name(self, key, value: str):
        if len(value) > 50 or len(value) < 1:
            raise ValueError("Last name must be within 1 to 50 characters")
        return value

    @validates('email')
    def validate_email(self, key, value):
        pattern = r"[a-zA-Z0-9.%-+]+@[a-zA-z0-9.-]+\.[a-zA-Z]{2,}"
        match = re.search(pattern, value)
        if match:
            return value
        else:
            raise ValueError("The email is not correct")

    @validates('password')
    def validate_password(self, key, password):
        """Hashes the password before storing it."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def add_place(self, place):
        self.places.append(place)
    
    def add_reviews(self, review):
        self.reviews.append(review)
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)        
    
