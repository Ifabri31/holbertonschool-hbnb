from app.models.basemodel import BaseModel
from app.models.user import User
from app.models.place import Place
from sqlalchemy.orm import validates, relationship
from app import db
from sqlalchemy import Column, Integer, ForeignKey

class Review(BaseModel):
    __tablename__ = 'reviews'

    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Relación con User
    user = db.relationship('User', back_populates='reviews')

    # Relación con Place
    place = db.relationship('Place', back_populates='reviews')

    def __init__(self, comment: str, rating: int, user_id: str, place_id: str):
        super().__init__()
        
        self.comment = comment
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        
    @validates('comment')
    def validate_comment(self, key, value: str):
        if value is None or len(value) == 0:
            raise ValueError("Comment cannot be empty")
        return value
        
    @validates('rating')
    def validate_rating(self, key, value: int):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value
