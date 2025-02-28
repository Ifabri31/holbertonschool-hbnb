from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user        
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        user_list = []
        exclude = ['created_at', 'updated_at', 'is_admin', 'places', 'reviews', 'password']
        for obj in self.user_repo.get_all():
            filtered_dict = {}
            for key, value in vars(obj).items():
                if key not in exclude:
                    filtered_dict[key] = value
            user_list.append(filtered_dict)
        return user_list

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if user:
            user.update(data)            
# _____________________________________________________________________________            
            
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place
    
    def get_place(self, place_id):
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        places_list = []
        exclude = ['description', 'owner', 'review', 'amenities', 'created_at', 'updated_at']
        for obj in self.place_repo.get_all():
            filtered_dict = {}
            for key, value in vars(obj).items():
                if key not in exclude:
                    filtered_dict[key] = value
            places_list.append(filtered_dict)
        return places_list

    def update_place(self, place_id, place_data):
        place = self.get(place_id)
        if place:
            place.update(place_data)
#_______________________________________________________________________________

    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review
    
    def get_review(self, review_id):
        return self.review_repo.get(review_id)
    
    def update_review(self, review_id, data):
        review = self.get(review_id)
        if review:
            review.update(data)
#________________________________________________________________________________

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
    
    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)

    def get_all_amenities(self):
        list_amenity = []
        for obj in self.amenity_repo.get_all():
            if isinstance(obj, Amenity):
                list_amenity.append(obj.name)
        return list_amenity


