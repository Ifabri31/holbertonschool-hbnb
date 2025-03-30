from app.models.basemodel import BaseModel
from app.models.user import User
from app.models.place import Place
from sqlalchemy.orm import validates, relationship
from app import db
from sqlalchemy import Column, Integer, ForeignKey

class Review(BaseModel):
    __tablename__ = 'reviews'

    comment = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='reviews')
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)
    place = relationship('Place', back_populates='reviews')

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
