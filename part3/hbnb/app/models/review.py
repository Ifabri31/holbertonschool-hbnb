from app.models.basemodel import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    def __init__(self, comment: str, rating: int, user_id: str, place_id: str):
        super().__init__()
        
        self.comment = comment
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        
    @property
    def comment(self) -> str:
        return self._comment
    @comment.setter
    def comment(self, value: str):
        if value is None or len(value) == 0:
            raise ValueError("Comment cannot be empty")
        self._comment = value
        
    @property
    def rating(self) -> int:
        return self._rating
    @rating.setter
    def rating(self, value: int):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value
