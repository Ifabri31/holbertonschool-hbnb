from app.models.basemodel import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    def __init__(self, comment: str, rating: int, user: User, place: Place):
        super().__init__()
        
        if comment is None or len(comment) == 0:
            raise ValueError("Comment cannot be empty")
        self.comment = comment
        
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        self.rating = rating

        # if user is None:
        #     raise ValueError
        self.user = user
        self.place = place
        
# Lorena = User("Lorena", "Leon", "dasd", "asd")        
# girasoles = Place("Girasoles", 20.0, 23.0, -120.0, Lorena)
# review = Review("todo bien", 5, Lorena, girasoles)

# print(review.place.price)